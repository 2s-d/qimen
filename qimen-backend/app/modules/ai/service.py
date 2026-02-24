# AI 模块业务逻辑：本地 GGUF 小模型（llama-cpp-python）对话服务

import os
import threading
import time
import subprocess
from typing import Any, Dict, List, Optional

from app.common.exceptions import BusinessException


SYSTEM_PROMPT = (
    "你叫「小奇」，是一个中文对话助手，风格温和、有耐心、解释清楚。\n"
    "你可以和用户聊天、解答各种日常问题，也可以聊奇门遁甲、占卜、传统文化等话题。\n"
    "当用户的问题涉及专业领域（比如奇门遁甲），请尽量结合常识和公开资料，给出结构清晰、步骤明确的说明。\n"
    "回答时尽量用简洁的口语化中文，可以分点列出要点；不要编造隐私信息，也不要做夸张的保证或承诺。\n"
)


_llm = None
_llm_lock = threading.Lock()
_infer_lock = threading.Lock()


def _default_model_path() -> str:
    # 默认使用你提供的模型文件名（放在 qimen-backend/models/ 下）
    return os.path.join("models", "qwen1_5-1_8b-chat-q4_0.gguf")


def _ollama_host() -> str:
    return os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")


def _ollama_model_name() -> str:
    # 给导入的 gguf 模型起一个固定名字，前后端都不用关心
    return os.getenv("AI_OLLAMA_MODEL", "wenxiaoqi-qwen1_5-1_8b")


def _ensure_ollama_running() -> None:
    """
    确保 Ollama 在本机运行。
    若没运行，尝试在后端进程内拉起 `ollama serve`（避免额外手动步骤）。
    """
    import requests

    host = _ollama_host().rstrip("/")
    try:
        r = requests.get(f"{host}/api/tags", timeout=1.5)
        if r.status_code == 200:
            return
    except Exception:
        pass

    # 尝试拉起 ollama serve（后台）
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
    except Exception as e:
        raise BusinessException(
            message=f"无法启动 Ollama（请确认已安装并加入 PATH）：{e}",
            code=500,
        ) from e

    # 等待服务起来
    for _ in range(25):
        try:
            r = requests.get(f"{host}/api/tags", timeout=1.5)
            if r.status_code == 200:
                return
        except Exception:
            time.sleep(0.2)

    raise BusinessException(message="Ollama 启动超时，请手动运行 `ollama serve` 后重试。", code=500)


def _ensure_ollama_model_exists(model_path: str) -> None:
    """
    确保 Ollama 中存在目标模型；若不存在，用本地 gguf 自动 create。
    """
    import requests

    _ensure_ollama_running()
    host = _ollama_host().rstrip("/")
    target = _ollama_model_name()

    try:
        tags = requests.get(f"{host}/api/tags", timeout=3).json()
        models = [m.get("name") for m in (tags.get("models") or [])]
        if target in models:
            return
    except Exception:
        # 如果 tags 失败，继续尝试 create
        pass

    # 生成 Modelfile（用相对路径 FROM ./xxx.gguf，便于可搬移）
    models_dir = os.path.dirname(model_path)
    gguf_filename = os.path.basename(model_path)
    modelfile_path = os.path.join(models_dir, "Modelfile.wenxiaoqi")

    system_line = SYSTEM_PROMPT.replace("\n", "\\n")
    modelfile = (
        f"FROM ./{gguf_filename}\n"
        f"SYSTEM \"{system_line}\"\n"
        "PARAMETER temperature 0.7\n"
        "PARAMETER top_p 0.9\n"
        "PARAMETER num_ctx 2048\n"
    )

    try:
        with open(modelfile_path, "w", encoding="utf-8") as f:
            f.write(modelfile)
    except Exception as e:
        raise BusinessException(message=f"写入 Modelfile 失败：{e}", code=500) from e

    # 调用 `ollama create`
    try:
        subprocess.check_call(
            ["ollama", "create", target, "-f", modelfile_path],
            cwd=models_dir,
        )
    except Exception as e:
        raise BusinessException(
            message=f"Ollama 导入 GGUF 失败：{e}。你也可以手动执行：cd {models_dir} && ollama create {target} -f {os.path.basename(modelfile_path)}",
            code=500,
        ) from e


def _get_llm():
    """
    懒加载模型：首次调用时加载 GGUF 到内存，避免后端启动阶段卡很久。
    """
    global _llm
    if _llm is not None:
        return _llm

    with _llm_lock:
        if _llm is not None:
            return _llm

        # 允许通过环境变量覆盖模型路径
        raw_path = os.getenv("AI_MODEL_PATH", _default_model_path())

        # 处理相对路径：优先按当前工作目录解析；若不存在，再按项目根目录解析
        model_path = raw_path
        if not os.path.isabs(model_path):
            if os.path.exists(model_path):
                model_path = os.path.abspath(model_path)
            else:
                here = os.path.dirname(os.path.abspath(__file__))
                # qimen-backend/app/modules/ai -> 上三级 = qimen-backend
                backend_root = os.path.abspath(os.path.join(here, "..", "..", ".."))
                model_path = os.path.join(backend_root, model_path)

        if not os.path.exists(model_path):
            raise BusinessException(
                message=f"AI模型文件不存在：{model_path}。请确认已将 .gguf 放入 qimen-backend/models/ 目录。",
                code=500,
            )

        # 先尝试 llama-cpp-python（真正“内置模型”）
        try:
            from llama_cpp import Llama  # type: ignore
        except Exception:
            # 若依赖不可用，则兜底走 Ollama（仍然由后端自动拉起/创建，避免用户额外步骤）
            _ensure_ollama_model_exists(model_path)
            return None

        # 推理参数：偏保守，保证在普通电脑上能跑
        n_threads = int(os.getenv("AI_N_THREADS", str(max((os.cpu_count() or 4) - 1, 1))))
        n_ctx = int(os.getenv("AI_N_CTX", "2048"))

        _llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=False,
        )

        return _llm


def _to_chat_messages(history: List[Dict[str, str]], question: str) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in history:
        role = m.get("role")
        content = (m.get("content") or "").strip()
        if role not in ("user", "assistant") or not content:
            continue
        messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": question.strip()})
    return messages


def chat(
    question: str,
    history: List[Dict[str, str]] | None = None,
    max_tokens: int | None = None,
) -> Dict[str, Any]:
    """
    返回：
    {
      "answer": "...",
      "history": [{"role":"user","content":"..."}, {"role":"assistant","content":"..."} ...]
    }
    """
    if not question or not question.strip():
        raise BusinessException(message="question 不能为空", code=400)

    history = history or []
    messages = _to_chat_messages(history, question)

    llm = _get_llm()

    # 生成长度：默认不“偷偷截断”，但仍然保留一个很高的安全上限，避免无限生成把服务卡死
    default_tokens = int(os.getenv("AI_MAX_TOKENS", "1024"))
    cap_tokens = int(os.getenv("AI_MAX_TOKENS_CAP", "2048"))
    effective_tokens = max_tokens if isinstance(max_tokens, int) and max_tokens > 0 else default_tokens
    if effective_tokens > cap_tokens:
        effective_tokens = cap_tokens
    if effective_tokens < 16:
        effective_tokens = 16

    # 1) 内置 llama-cpp 路径
    if llm is not None:
        with _infer_lock:
            try:
                resp = llm.create_chat_completion(  # type: ignore[attr-defined]
                    messages=messages,
                    temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
                    top_p=float(os.getenv("AI_TOP_P", "0.9")),
                    # 默认给足一点长度，避免内容被截断；如需调整可通过环境变量 AI_MAX_TOKENS 覆盖
                    max_tokens=effective_tokens,
                )
                answer = (
                    resp.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                ).strip()
            except Exception as e:
                raise BusinessException(message=f"AI生成失败：{str(e)}", code=500) from e
    else:
        # 2) Ollama 兜底路径
        import requests

        _ensure_ollama_running()
        host = _ollama_host().rstrip("/")
        model = _ollama_model_name()

        temperature = float(os.getenv("AI_TEMPERATURE", "0.7"))
        top_p = float(os.getenv("AI_TOP_P", "0.9"))

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                # 控制生成长度，避免本地小模型输出过长导致卡死/超时
                "num_predict": effective_tokens,
                "temperature": temperature,
                "top_p": top_p,
            },
        }
        with _infer_lock:
            try:
                # 首次调用本地模型可能较慢，适当放宽超时时间
                r = requests.post(f"{host}/api/chat", json=payload, timeout=600)
                r.raise_for_status()
                data = r.json()
                answer = (data.get("message", {}) or {}).get("content", "").strip()
            except Exception as e:
                raise BusinessException(message=f"Ollama 调用失败：{e}", code=500) from e

    if not answer:
        answer = "我暂时没想好怎么回答。你可以换一种问法（例如：从八门、九星、八神、九宫格局来问）。"

    new_history = list(history)
    new_history.append({"role": "user", "content": question.strip()})
    new_history.append({"role": "assistant", "content": answer})

    # 控制历史长度，避免越聊越慢（保留最后 N 轮）
    max_turns = int(os.getenv("AI_MAX_TURNS", "8"))
    # 每轮两条消息：user+assistant
    if max_turns > 0 and len(new_history) > max_turns * 2:
        new_history = new_history[-max_turns * 2 :]

    return {"answer": answer, "history": new_history}


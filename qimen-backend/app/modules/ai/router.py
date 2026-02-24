# AI 路由：问小奇对话接口

from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool

from app.common.response import success_response
from app.modules.ai.schemas import AIChatRequest
from app.modules.ai import service


router = APIRouter()


@router.post("/chat", summary="问小奇 - AI对话")
async def ai_chat(request: AIChatRequest):
    """
    POST /api/ai/chat
    - 前端传入 question + history
    - 后端使用本地 GGUF 小模型生成 answer
    """
    # llama-cpp / requests 调用 Ollama 都是阻塞型；放到线程池里避免卡死整个 event loop
    data = await run_in_threadpool(
        service.chat,
        request.question,
        [m.model_dump() for m in (request.history or [])],
        request.max_tokens,
    )
    return success_response(data=data)


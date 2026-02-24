# AI 模块 schemas

from typing import Literal, List, Optional
from pydantic import BaseModel, Field


class AIChatMessage(BaseModel):
    role: Literal["user", "assistant"] = Field(..., description="消息角色")
    content: str = Field(..., min_length=1, description="消息内容")


class AIChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="用户问题")
    history: List[AIChatMessage] = Field(default_factory=list, description="历史对话（不含system）")
    max_tokens: Optional[int] = Field(
        default=None,
        ge=16,
        le=2048,
        description="最大生成长度（token 数）。不传则使用默认值。",
    )


class AIChatData(BaseModel):
    answer: str = Field(..., description="AI回答")
    history: List[AIChatMessage] = Field(..., description="更新后的历史对话")


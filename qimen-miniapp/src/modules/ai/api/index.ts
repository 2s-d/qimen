// 问小琪 - AI 对话接口
// 后端：POST /api/ai/chat

import { request } from '@/common/utils/request'

export interface AIChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface AIChatResponse {
  answer: string
  history: AIChatMessage[]
}

export const aiChat = (data: { question: string; history: AIChatMessage[]; max_tokens?: number }) => {
  return request<AIChatResponse>({
    url: '/ai/chat',
    method: 'POST',
    data,
    // AI 对话页面自己做“正在思考”提示，这里关闭全局居中 loading 遮罩
    loading: false
  })
}


// 文档引用：PROJECT_SPEC.md - 1288行
// 算命模块API

import { request } from '@/common/utils/request'

/**
 * 起盘计算
 * POST /api/qimen/calculate
 * 文档引用：PROJECT_SPEC.md - 5.2.1节
 */
export const calculateQimen = (data: {
  datetime: string
  gender: '男' | '女'
  type: '时家奇门' | '日家奇门'
  calendar_type?: '公历' | '农历'
}) => {
  return request({
    url: '/qimen/calculate',
    method: 'POST',
    data
  })
}

/**
 * 保存起盘记录
 * POST /api/qimen/save
 * 文档引用：PROJECT_SPEC.md - 5.2.2节
 */
export const saveQimenRecord = (data: any) => {
  return request({
    url: '/qimen/save',
    method: 'POST',
    data
  })
}

/**
 * 获取历史记录列表
 * GET /api/qimen/history
 * 文档引用：PROJECT_SPEC.md - 5.2.3节
 */
export const getHistoryList = (params?: { page?: number; size?: number }) => {
  return request({
    url: '/qimen/history',
    method: 'GET',
    data: params
  })
}

/**
 * 获取历史记录详情
 * GET /api/qimen/history/:id
 * 文档引用：PROJECT_SPEC.md - 5.2.4节
 */
export const getHistoryDetail = (id: number) => {
  return request({
    url: `/qimen/history/${id}`,
    method: 'GET'
  })
}

/**
 * 删除历史记录
 * DELETE /api/qimen/history/:id
 * 文档引用：PROJECT_SPEC.md - 5.2.5节
 */
export const deleteHistoryRecord = (id: number) => {
  return request({
    url: `/qimen/history/${id}`,
    method: 'DELETE'
  })
}

/**
 * 获取今日运势
 * GET /api/qimen/fortune
 * 文档引用：PROJECT_SPEC.md - 5.2.6节
 */
export const getDailyFortune = (date?: string) => {
  return request({
    url: '/qimen/fortune',
    method: 'GET',
    data: date ? { date } : {}
  })
}

/**
 * 获取万年历数据
 * GET /api/tools/calendar
 * 文档引用：PROJECT_SPEC.md - 5.2.7节
 */
export const getCalendarData = (year: number, month: number) => {
  return request({
    url: '/tools/calendar',
    method: 'GET',
    data: { year, month }
  })
}

/**
 * 获取知识文章
 * GET /api/knowledge/articles
 * 文档引用：PROJECT_SPEC.md - 5.2.8节
 */
export const getKnowledgeArticles = (category?: string) => {
  return request({
    url: '/knowledge/articles',
    method: 'GET',
    data: { category }
  })
}

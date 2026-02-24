// 文档引用：PROJECT_SPEC.md - 1303行
// 系统模块API

import { request } from '@/common/utils/request'

/**
 * 获取系统配置
 * GET /api/system/config
 * 文档引用：PROJECT_SPEC.md - 5.3.1节
 */
export const getSystemConfig = () => {
  return request({
    url: '/system/config',
    method: 'GET'
  })
}

/**
 * 获取帮助文档
 * GET /api/system/help
 * 文档引用：PROJECT_SPEC.md - 5.3.2节
 */
export const getHelpDoc = () => {
  return request({
    url: '/system/help',
    method: 'GET'
  })
}

/**
 * 提交意见反馈
 * POST /api/system/feedback
 * 文档引用：PROJECT_SPEC.md - 5.3.3节
 */
export const submitFeedback = (data: { content: string; contact?: string }) => {
  return request({
    url: '/system/feedback',
    method: 'POST',
    data
  })
}

/**
 * 获取公告列表
 * GET /api/system/announcements
 * 文档引用：PROJECT_SPEC.md - 5.3.4节
 */
export const getAnnouncements = () => {
  return request({
    url: '/system/announcements',
    method: 'GET'
  })
}

/**
 * 获取数据统计
 * GET /api/system/statistics
 * 文档引用：PROJECT_SPEC.md - 5.3.5节
 */
export const getStatistics = () => {
  return request({
    url: '/system/statistics',
    method: 'GET'
  })
}

/**
 * 健康检查
 * GET /api/system/health
 * 文档引用：PROJECT_SPEC.md - 5.3.6节
 */
export const checkHealth = () => {
  return request({
    url: '/system/health',
    method: 'GET'
  })
}

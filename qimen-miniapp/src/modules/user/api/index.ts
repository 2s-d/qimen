// 文档引用：PROJECT_SPEC.md - 1272行
// 用户模块API

import { request } from '@/common/utils/request'

/**
 * 用户注册
 * POST /api/user/register
 * 文档引用：PROJECT_SPEC.md - 5.1.1节
 */
export const registerUser = (data: {
  username: string
  password: string
  nickname?: string
}) => {
  return request({
    url: '/user/register',
    method: 'POST',
    data
  })
}

/**
 * 用户登录
 * POST /api/user/login
 * 文档引用：PROJECT_SPEC.md - 5.1.2节
 */
export const loginUser = (data: {
  username: string
  password: string
}) => {
  return request({
    url: '/user/login',
    method: 'POST',
    data
  })
}

/**
 * 获取用户信息
 * GET /api/user/info
 * 文档引用：PROJECT_SPEC.md - 5.1.3节
 */
export const getUserInfo = () => {
  return request({
    url: '/user/info',
    method: 'GET'
  })
}

/**
 * 修改用户信息
 * PUT /api/user/info
 * 文档引用：PROJECT_SPEC.md - 5.1.4节
 */
export const updateUserInfo = (data: {
  nickname: string
}) => {
  return request({
    url: '/user/info',
    method: 'PUT',
    data
  })
}

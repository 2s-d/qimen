// 文档引用：PROJECT_SPEC.md - 1276行
// 认证工具

import { getToken, removeToken } from '@/common/utils/storage'

/**
 * 检查用户是否已登录
 * @returns {boolean}
 */
export const checkLogin = (): boolean => {
  const token = getToken()
  return !!token
}

/**
 * 获取当前登录用户的Token
 * @returns {string|null}
 */
export const getUserToken = (): string | null => {
  return getToken()
}

/**
 * 重定向到登录页
 */
export const redirectToLogin = (): void => {
  // 清除可能的过期token
  removeToken()
  uni.navigateTo({
    url: '/pages/login/index'
  })
}

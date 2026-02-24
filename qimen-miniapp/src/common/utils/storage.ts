// 文档引用：PROJECT_SPEC.md - 1320行
// 本地存储封装（token、缓存管理）

import { TOKEN_KEY, USER_INFO_KEY } from './constants'

/**
 * 存储数据
 */
export const setStorage = (key: string, value: any): void => {
  try {
    uni.setStorageSync(key, value)
  } catch (e) {
    console.error('存储失败:', e)
  }
}

/**
 * 获取数据
 */
export const getStorage = (key: string): any => {
  try {
    return uni.getStorageSync(key)
  } catch (e) {
    console.error('获取存储失败:', e)
    return null
  }
}

/**
 * 删除数据
 */
export const removeStorage = (key: string): void => {
  try {
    uni.removeStorageSync(key)
  } catch (e) {
    console.error('删除存储失败:', e)
  }
}

/**
 * 清空所有数据
 */
export const clearStorage = (): void => {
  try {
    uni.clearStorageSync()
  } catch (e) {
    console.error('清空存储失败:', e)
  }
}

/**
 * 设置带过期时间的缓存
 */
export const setCache = (key: string, value: any, expireSeconds: number = 3600): void => {
  const expireTime = Date.now() + expireSeconds * 1000
  setStorage(key, {
    value,
    expireTime
  })
}

/**
 * 获取缓存（自动检查过期）
 */
export const getCache = (key: string): any => {
  const cached = getStorage(key)
  if (!cached) {
    return null
  }
  
  if (Date.now() > cached.expireTime) {
    removeStorage(key)
    return null
  }
  
  return cached.value
}

// Token相关快捷方法
export const setToken = (token: string): void => setStorage(TOKEN_KEY, token)
export const getToken = (): string | null => getStorage(TOKEN_KEY)
export const removeToken = (): void => removeStorage(TOKEN_KEY)

// 用户信息相关快捷方法
export const setUserInfo = (userInfo: any): void => setStorage(USER_INFO_KEY, userInfo)
export const getUserInfo = (): any => getStorage(USER_INFO_KEY)
export const removeUserInfo = (): void => removeStorage(USER_INFO_KEY)

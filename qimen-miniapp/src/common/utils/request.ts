// 文档引用：PROJECT_SPEC.md - 1317行
// 请求封装

import { API_BASE_URL } from './constants'
import { getToken } from './storage'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: Record<string, string>
  loading?: boolean
  loadingText?: string
}

/**
 * 统一请求封装
 * 文档引用：PROJECT_SPEC.md - 6.1.4节、6.2.2节
 */
export const request = <T = any>(options: RequestOptions): Promise<T> => {
  return new Promise((resolve, reject) => {
    try {
      // 请求拦截：添加token到header
      const token = getToken()
      let url = options.url.startsWith('http') ? options.url : `${API_BASE_URL}${options.url}`
      const method = options.method || 'GET'
      
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...options.header
      }
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
      
      // 为了避免浏览器 / 代理层返回 304（导致没有响应体而本封装按失败处理），
      // 对 GET 请求追加时间戳参数，强制拿到 200 响应
      if (method === 'GET' && !url.includes('_t=')) {
        const sep = url.includes('?') ? '&' : '?'
        url = `${url}${sep}_t=${Date.now()}`
      }

      // 显示loading
      if (options.loading !== false) {
        uni.showLoading({
          title: options.loadingText || '加载中...',
          mask: true
        })
      }
      
      uni.request({
        url,
        method,
        data: options.data || {},
        header: headers,
        success: (res) => {
          // 隐藏loading
          if (options.loading !== false) {
            uni.hideLoading()
          }
          
          // 统一处理响应格式（文档6.1.4节）
          if (res.statusCode === 200) {
            const { code, message, data } = res.data as any
            if (code === 200) {
              resolve(data) // 成功时直接返回data
            } else {
              // 错误时显示Toast并抛出异常
              uni.showToast({
                title: message || '请求失败',
                icon: 'none',
                duration: 2000
              })
              reject(new Error(message || '请求失败'))
            }
          } else {
            // 网络错误
            uni.showToast({
              title: '网络请求失败',
              icon: 'none',
              duration: 2000
            })
            reject(new Error('网络请求失败'))
          }
        },
        fail: (err) => {
          // 隐藏loading
          if (options.loading !== false) {
            uni.hideLoading()
          }
          
          // 网络错误处理
          uni.showToast({
            title: '网络请求失败',
            icon: 'none',
            duration: 2000
          })
          reject(err)
        }
      })
    } catch (error) {
      // 确保在异常情况下也隐藏loading
      if (options.loading !== false) {
        uni.hideLoading()
      }
      console.error('请求异常:', error)
      reject(error)
    }
  })
}

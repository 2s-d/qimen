// 文档引用：PROJECT_SPEC.md - 1321行
// 常量定义

// API 基础地址：根据运行环境自动切换
// - 本地 H5 调试：直接打本机后端 http://localhost:8087/api
// - 部署到服务器的 H5（域名 qimen.paku.uno）：走相对路径 /api，由 Nginx 反向代理到后端
// - 小程序 / App 等非 H5 平台：直接访问公网后端 https://qimen.paku.uno/api
let base = 'http://localhost:8087/api'
// @ts-ignore uni-compiler 会注入平台标识
const platform = typeof uni !== 'undefined' ? uni.getSystemInfoSync().platform : ''

// H5 环境通过 window.location 判断是否已在公网域名下
if (typeof window !== 'undefined') {
  const host = window.location.host
  if (host.includes('qimen.paku.uno')) {
    // 部署在服务器上的 H5：与前端同域，用相对路径 /api 即可，由 Nginx 代理到后端
    base = '/api'
  } else {
    // 本地 H5 调试
    base = 'http://localhost:8087/api'
  }
} else {
  // 非 H5（如小程序 / App），统一走公网后端域名
  base = 'https://qimen.paku.uno/api'
}

export const API_BASE_URL = base // API基础地址
export const TOKEN_KEY = 'qimen_token' // token存储key
export const USER_INFO_KEY = 'qimen_user_info' // 用户信息存储key
export const PAGE_SIZE = 10 // 分页大小10
export const MAX_HISTORY = 100 // 最大历史记录数100

// 12时辰列表
export const SHICHEN_LIST = [
  { label: '子时', value: '子', range: '23:00-01:00' },
  { label: '丑时', value: '丑', range: '01:00-03:00' },
  { label: '寅时', value: '寅', range: '03:00-05:00' },
  { label: '卯时', value: '卯', range: '05:00-07:00' },
  { label: '辰时', value: '辰', range: '07:00-09:00' },
  { label: '巳时', value: '巳', range: '09:00-11:00' },
  { label: '午时', value: '午', range: '11:00-13:00' },
  { label: '未时', value: '未', range: '13:00-15:00' },
  { label: '申时', value: '申', range: '15:00-17:00' },
  { label: '酉时', value: '酉', range: '17:00-19:00' },
  { label: '戌时', value: '戌', range: '19:00-21:00' },
  { label: '亥时', value: '亥', range: '21:00-23:00' }
]

// 运势类型：事业/财运/感情/健康
export const FORTUNE_TYPES = ['career', 'wealth', 'love', 'health'] as const

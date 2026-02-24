// 文档引用：PROJECT_SPEC.md - 1305行
// 系统模块状态管理

import { defineStore } from 'pinia'
import { getSystemConfig as fetchSystemConfig, getAnnouncements as fetchAnnouncements, getHelpDoc as fetchHelpDoc, submitFeedback as apiSubmitFeedback, getStatistics as apiGetStatistics, checkHealth as apiCheckHealth } from '../api/index'
import { setCache, getCache } from '@/common/utils/storage'

const SYSTEM_CONFIG_CACHE_KEY = 'system_config_cache'
const ANNOUNCEMENTS_CACHE_KEY = 'announcements_cache'
const HELP_DOC_CACHE_KEY = 'help_doc_cache'

export const useSystemStore = defineStore('system', {
  state: () => ({
    config: null as any,
    announcements: [] as any[],
    banners: [] as any[],
    helpDoc: null as any
  }),
  getters: {
    getAppVersion: (state) => state.config?.app_version || '1.0.0',
    getAppName: (state) => state.config?.app_name || '奇门遁甲',
    getBannerImages: (state) => state.banners.length > 0 ? state.banners : [],
    getAnnouncementsList: (state) => state.announcements,
    getContactEmail: (state) => state.config?.contact_email || 'contact@example.com',
    getAboutText: (state) => state.config?.about_text || '这是一款基于奇门遁甲的在线算命工具...',
    getDisclaimer: (state) => state.config?.disclaimer || '本应用仅供娱乐参考，不构成任何专业建议...'
  },
  actions: {
    async getSystemConfig() {
      // 检查缓存
      const cachedConfig = getCache(SYSTEM_CONFIG_CACHE_KEY)
      if (cachedConfig) {
        this.config = cachedConfig
        // banner_images 可能是数组，也可能是 { images: [...] }，这里统一转成数组
        const bannerCfg = cachedConfig.banner_images
        this.banners = Array.isArray(bannerCfg) ? bannerCfg : (bannerCfg?.images || [])
        return cachedConfig
      }
      try {
        const res = await fetchSystemConfig()
        this.config = res
        const bannerCfg = res.banner_images
        this.banners = Array.isArray(bannerCfg) ? bannerCfg : (bannerCfg?.images || [])
        // 缓存1小时（文档引用：PROJECT_SPEC.md - 4089行）
        setCache(SYSTEM_CONFIG_CACHE_KEY, res, 3600)
        return res
      } catch (error) {
        console.error('获取系统配置失败:', error)
        // 提供默认配置
        this.config = {
          app_version: '1.0.0',
          app_name: '奇门遁甲',
          banner_images: [],
          contact_email: 'contact@example.com',
          about_text: '这是一款基于奇门遁甲的在线算命工具...',
          disclaimer: '本应用仅供娱乐参考，不构成任何专业建议...'
        }
        this.banners = []
        throw error
      }
    },
    async getAnnouncements() {
      // 检查缓存（缓存5分钟）
      const cachedAnnouncements = getCache(ANNOUNCEMENTS_CACHE_KEY)
      if (cachedAnnouncements) {
        this.announcements = cachedAnnouncements
        return cachedAnnouncements
      }
      try {
        const res = await fetchAnnouncements()
        this.announcements = res || []
        // 缓存5分钟
        setCache(ANNOUNCEMENTS_CACHE_KEY, res, 300)
        return res
      } catch (error) {
        console.error('获取公告失败:', error)
        this.announcements = []
        throw error
      }
    },
    async getHelpDoc() {
      // 检查缓存（缓存24小时）
      const cachedHelpDoc = getCache(HELP_DOC_CACHE_KEY)
      if (cachedHelpDoc) {
        this.helpDoc = cachedHelpDoc
        return cachedHelpDoc
      }
      try {
        const res = await fetchHelpDoc()
        this.helpDoc = res
        // 缓存24小时
        setCache(HELP_DOC_CACHE_KEY, res, 3600 * 24)
        return res
      } catch (error) {
        console.error('获取帮助文档失败:', error)
        this.helpDoc = { questions: [] }
        throw error
      }
    },
    async submitFeedback(data: { content: string; contact?: string }) {
      try {
        await apiSubmitFeedback(data)
        uni.showToast({ title: '反馈成功', icon: 'success' })
      } catch (error) {
        console.error('提交反馈失败:', error)
        throw error
      }
    },
    async getStatistics() {
      try {
        const res = await apiGetStatistics()
        return res
      } catch (error) {
        console.error('获取统计数据失败:', error)
        throw error
      }
    },
    async checkHealth() {
      try {
        const res = await apiCheckHealth()
        return res
      } catch (error) {
        console.error('健康检查失败:', error)
        throw error
      }
    }
  }
})

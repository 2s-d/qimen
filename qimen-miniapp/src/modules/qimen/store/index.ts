// 文档引用：PROJECT_SPEC.md - 1290行
// 算命模块状态管理

import { defineStore } from 'pinia'
import { calculateQimen as apiCalculateQimen, saveQimenRecord as apiSaveQimenRecord, getHistoryList as apiGetHistoryList, getHistoryDetail as apiGetHistoryDetail, deleteHistoryRecord as apiDeleteHistoryRecord, getDailyFortune as apiGetDailyFortune, getCalendarData as apiGetCalendarData, getKnowledgeArticles as apiGetKnowledgeArticles } from '../api/index'
import { getCache, setCache } from '@/common/utils/storage'
import { formatDate } from '@/common/utils/format'

const DAILY_FORTUNE_CACHE_KEY = 'daily_fortune_cache_'

export const useQimenStore = defineStore('qimen', {
  state: () => ({
    currentPlate: null as any,
    historyList: [] as any[],
    dailyFortune: null as any,
    knowledgeArticles: [] as any[],
    prefillInput: null as any,
    pagination: {
      page: 1,
      size: 10,
      total: 0
    }
  }),
  getters: {
    hasCurrentPlate: (state) => !!state.currentPlate,
    historyCount: (state) => state.pagination.total
  },
  actions: {
    async calculateQimen(params: {
      datetime: string
      gender: '男' | '女'
      type: '时家奇门' | '日家奇门'
      calendar_type?: '公历' | '农历'
    }) {
      try {
        const res = await apiCalculateQimen(params)
        this.currentPlate = res
        return res
      } catch (error) {
        console.error('起盘计算失败:', error)
        throw error
      }
    },
    async saveQimenRecord(recordData: any) {
      try {
        const res = await apiSaveQimenRecord(recordData)
        uni.showToast({ title: '保存成功', icon: 'success' })
        return res
      } catch (error) {
        console.error('保存记录失败:', error)
        throw error
      }
    },
    async getHistoryList(params: { page?: number; size?: number; append?: boolean } = {}) {
      try {
        const { append, ...query } = params as any
        const res = await apiGetHistoryList(query)
        const items = res.items || []
        this.historyList = append ? [...this.historyList, ...items] : items
        this.pagination.total = res.total || 0
        this.pagination.page = res.page || 1
        this.pagination.size = res.size || 10
        return res
      } catch (error) {
        console.error('获取历史记录列表失败:', error)
        this.historyList = []
        this.pagination.total = 0
        throw error
      }
    },
    async getHistoryDetail(id: number) {
      try {
        const res = await apiGetHistoryDetail(id)
        return res
      } catch (error) {
        console.error('获取历史记录详情失败:', error)
        throw error
      }
    },
    async deleteHistoryRecord(id: number) {
      try {
        await apiDeleteHistoryRecord(id)
        this.historyList = this.historyList.filter(item => item.id !== id)
        this.pagination.total--
        uni.showToast({ title: '删除成功', icon: 'success' })
      } catch (error) {
        console.error('删除历史记录失败:', error)
        throw error
      }
    },
    async getDailyFortune(date?: Date | string) {
      // 文档引用：PROJECT_SPEC.md - 177行，今日运势每日更新，缓存当天数据
      const today = formatDate(date || new Date(), 'YYYY-MM-DD')
      const cacheKey = DAILY_FORTUNE_CACHE_KEY + today
      const cachedFortune = getCache(cacheKey)

      if (cachedFortune) {
        this.dailyFortune = cachedFortune
        return cachedFortune
      }

      try {
        const res = await apiGetDailyFortune(today)
        this.dailyFortune = res
        // 缓存到当天结束（文档引用：PROJECT_SPEC.md - 3671行）
        const endOfDay = new Date(today)
        endOfDay.setHours(23, 59, 59, 999)
        const expireSeconds = Math.floor((endOfDay.getTime() - Date.now()) / 1000)
        if (expireSeconds > 0) {
          setCache(cacheKey, res, expireSeconds)
        }
        return res
      } catch (error) {
        console.error('获取今日运势失败:', error)
        this.dailyFortune = null
        throw error
      }
    },
    async getCalendarData(year: number, month: number) {
      try {
        const res = await apiGetCalendarData(year, month)
        return res
      } catch (error) {
        console.error('获取万年历数据失败:', error)
        throw error
      }
    },
    async getKnowledgeArticles(category?: string) {
      try {
        const res = await apiGetKnowledgeArticles(category)
        this.knowledgeArticles = res || []
        return res
      } catch (error) {
        console.error('获取知识文章失败:', error)
        this.knowledgeArticles = []
        throw error
      }
    },
    clearCurrentPlate() {
      this.currentPlate = null
    }
    ,
    setPrefillInput(payload: any) {
      this.prefillInput = payload
    },
    clearPrefillInput() {
      this.prefillInput = null
    }
  }
})

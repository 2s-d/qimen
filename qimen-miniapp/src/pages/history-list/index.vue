<!-- 文档引用：PROJECT_SPEC.md - 2.2.7节 -->
<!-- 页面7：历史记录列表页 -->
<!-- UI模板参考：template/7-history-list.html -->

<template>
  <view class="history-list-page">
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">历史记录</text>
    </view>

    <!-- 未登录：显示“请先登录”卡片 -->
    <view v-if="!isLogin" class="not-login-wrapper">
      <view class="not-login-card">
        <view class="not-login-icon">👤</view>
        <text class="not-login-text">请先登录后查看历史记录</text>
        <button class="login-btn" @click="goLogin">立即登录</button>
      </view>
    </view>

    <!-- 已登录：显示历史列表 -->
    <scroll-view v-else class="content" scroll-y @scrolltolower="loadMore">
      <view v-if="loading && records.length === 0" class="loading">
        <text class="loading-text">加载中...</text>
      </view>

      <view v-else-if="records.length === 0" class="empty-state">
        <view class="empty-icon">📭</view>
        <view class="empty-text">暂无历史记录</view>
        <view class="empty-btn" @click="goInput">立即起盘</view>
      </view>

      <view v-else>
        <HistoryCard
          v-for="item in records"
          :key="item.id"
          :record="item"
          @view="viewDetail"
          @delete="confirmDelete"
        />

        <view class="load-tip" v-if="loadingMore">
          <text class="loading-text">加载中...</text>
        </view>
        <view class="load-tip" v-else-if="finished">
          <text class="loading-text">没有更多了</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow, onPullDownRefresh } from '@dcloudio/uni-app'
import { useUserStore } from '@/modules/user/store/index'
import { useQimenStore } from '@/modules/qimen/store/index'
import HistoryCard from '@/modules/qimen/components/HistoryCard.vue'
import { formatDateTime, formatStar } from '@/common/utils/format'

const userStore = useUserStore()
const qimenStore = useQimenStore()
const isLogin = computed(() => userStore.loggedIn)

const loading = ref(false)
const loadingMore = ref(false)
const finished = ref(false)
const page = ref(1)
const size = ref(10)
const records = ref<any[]>([])

const goLogin = () => {
  uni.navigateTo({
    url: `/pages/login/index?redirect=${encodeURIComponent('/pages/history-list/index')}`
  })
}

const handleBack = () => {
  // 兼容 tabbar 根页：如果当前就是历史 tab 的根页面，没有可返回历史，则回到首页 tab
  try {
    // eslint-disable-next-line no-undef
    const pages = getCurrentPages && getCurrentPages()
    const len = Array.isArray(pages) ? pages.length : 0
    if (!len || len <= 1) {
      uni.switchTab({ url: '/pages/index/index' })
      return
    }
  } catch {
    // ignore
  }
  uni.navigateBack({
    fail() {
      uni.switchTab({ url: '/pages/index/index' })
    }
  })
}

const normalizeList = (items: any[]) => {
  return items.map((x) => {
    const dt = x.datetime || x.created_at
    const score = x.fortune_score
    return {
      ...x,
      display_time: dt ? `📅 ${dt}` : '📅 --',
      gender_text: x.gender,
      type_text: x.type,
      fortune_text: score ? `${formatStar(score)} ${score}分` : '--'
    }
  })
}

const fetchFirstPage = async () => {
  loading.value = true
  finished.value = false
  page.value = 1
  try {
    const res = await qimenStore.getHistoryList({ page: page.value, size: size.value, append: false })
    records.value = normalizeList(res.items || [])
    const total = res.total || 0
    finished.value = records.value.length >= total
  } catch {
    records.value = []
  } finally {
    loading.value = false
    uni.stopPullDownRefresh()
  }
}

const loadMore = async () => {
  if (loadingMore.value || finished.value || loading.value) return
  loadingMore.value = true
  try {
    const next = page.value + 1
    const res = await qimenStore.getHistoryList({ page: next, size: size.value, append: true })
    page.value = next
    const more = normalizeList(res.items || [])
    records.value = [...records.value, ...more]
    const total = res.total || 0
    finished.value = records.value.length >= total
  } catch {
    // ignore
  } finally {
    loadingMore.value = false
  }
}

const viewDetail = (item: any) => {
  uni.navigateTo({ url: `/pages/history-detail/index?id=${item.id}` })
}

const confirmDelete = (item: any) => {
  uni.showModal({
    title: '提示',
    content: '确定删除该记录吗？',
    success: async (res) => {
      if (!res.confirm) return
      try {
        await qimenStore.deleteHistoryRecord(item.id)
        records.value = records.value.filter(x => x.id !== item.id)
      } catch {
        // request.ts 已统一toast
      }
    }
  })
}

const goInput = () => {
  uni.switchTab({ url: '/pages/qimen-input/index' })
}

onPullDownRefresh(fetchFirstPage)

onShow(() => {
  if (!isLogin.value) {
    // 未登录时只显示提示卡片，不自动跳转登录页
    return
  }
  fetchFirstPage()
})
</script>

<style scoped>
.history-list-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f5f5f5;
}

.not-login-wrapper {
  flex: 1;
  padding: 40rpx 30rpx;
}

.not-login-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 60rpx 40rpx;
  text-align: center;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.not-login-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
}

.not-login-text {
  display: block;
  font-size: 30rpx;
  color: #333;
  margin-bottom: 40rpx;
}

.login-btn {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 44rpx;
  font-size: 30rpx;
  font-weight: bold;
}

.navbar {
  background: #fff;
  min-height: 88rpx;
  padding-top: constant(safe-area-inset-top);
  padding-top: env(safe-area-inset-top);
  display: flex;
  align-items: center;
  padding-left: 30rpx;
  padding-right: 30rpx;
  box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-btn {
  font-size: 36rpx;
  color: #667eea;
}

.nav-title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-size: 34rpx;
  font-weight: 500;
  color: #333;
}

.content {
  flex: 1;
  padding: 30rpx;
  height: 0;
}

.loading,
.load-tip {
  text-align: center;
  padding: 30rpx 0;
}

.loading-text {
  font-size: 26rpx;
  color: #999;
}

.empty-state {
  text-align: center;
  padding: 160rpx 40rpx;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 40rpx;
}

.empty-text {
  font-size: 30rpx;
  color: #999;
  margin-bottom: 50rpx;
}

.empty-btn {
  display: inline-block;
  padding: 24rpx 60rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  font-size: 30rpx;
}
</style>

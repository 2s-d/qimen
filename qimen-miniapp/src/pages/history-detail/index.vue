<!-- 文档引用：PROJECT_SPEC.md - 2.2.8节 -->
<!-- 页面8：历史记录详情页 -->
<!-- UI模板参考：template/8-history-detail.html -->

<template>
  <view class="history-detail-page">
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">历史详情</text>
    </view>

    <scroll-view class="content" scroll-y>
      <view class="info-bar" v-if="detail">
        📅 {{ detail.datetime }}<br />
        👤 {{ detail.gender }} | 🔮 {{ detail.type }}
      </view>

      <view class="plate-container" v-if="detail">
        <PlateGrid :palaces="palaces" @select="openPalace" />
      </view>

      <view class="result-section" v-if="detail">
        <view class="section-title">运势解读</view>
        <view class="fortune-item">
          <view class="fortune-name">总体运势</view>
          <view class="fortune-stars">{{ starText(detail.fortune_score) }} {{ detail.fortune_score }}分</view>
        </view>
        <view class="fortune-item">
          <view class="fortune-name">💼 事业运</view>
          <view class="fortune-stars">{{ starText(detail.fortune_data?.fortunes?.career?.score) }}</view>
        </view>
        <view class="fortune-item">
          <view class="fortune-name">💰 财运</view>
          <view class="fortune-stars">{{ starText(detail.fortune_data?.fortunes?.wealth?.score) }}</view>
        </view>
        <view class="fortune-item">
          <view class="fortune-name">💕 感情运</view>
          <view class="fortune-stars">{{ starText(detail.fortune_data?.fortunes?.love?.score) }}</view>
        </view>
        <view class="fortune-item">
          <view class="fortune-name">🏥 健康运</view>
          <view class="fortune-stars">{{ starText(detail.fortune_data?.fortunes?.health?.score) }}</view>
        </view>
      </view>

      <view class="action-buttons" v-if="detail">
        <button class="btn btn-primary" @click="reQimen">重新起盘</button>
        <button class="btn btn-danger" @click="confirmDelete">删除记录</button>
      </view>

      <view v-if="loading" class="loading">
        <text class="loading-text">加载中...</text>
      </view>
    </scroll-view>

    <PalaceDetail :visible="palaceVisible" :palace="selectedPalace" @close="closePalace" />
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/modules/user/store/index'
import { useQimenStore } from '@/modules/qimen/store/index'
import PlateGrid from '@/modules/qimen/components/PlateGrid.vue'
import PalaceDetail from '@/modules/qimen/components/PalaceDetail.vue'
import { formatStar } from '@/common/utils/format'

const userStore = useUserStore()
const qimenStore = useQimenStore()

const isLogin = computed(() => userStore.loggedIn)
const lastAutoRedirectAt = ref(0)

const id = ref<number>(0)
const detail = ref<any | null>(null)
const loading = ref(false)

const palaceVisible = ref(false)
const selectedPalace = ref<any | null>(null)

onLoad((options) => {
  id.value = Number(options?.id || 0)
})

const goLogin = () => {
  uni.navigateTo({
    url: `/pages/login/index?redirect=${encodeURIComponent(`/pages/history-detail/index?id=${id.value}`)}`
  })
}

const fetchDetail = async () => {
  if (!id.value) return
  loading.value = true
  try {
    detail.value = await qimenStore.getHistoryDetail(id.value)
  } catch {
    detail.value = null
  } finally {
    loading.value = false
  }
}

onShow(() => {
  if (!isLogin.value) {
    const now = Date.now()
    if (now - lastAutoRedirectAt.value > 2500) {
      lastAutoRedirectAt.value = now
      goLogin()
    }
    return
  }
  fetchDetail()
})

const palaces = computed(() => detail.value?.plate_data?.palaces || [])

const handleBack = () => {
  uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/history-list/index' }) })
}

const openPalace = (p: any) => {
  selectedPalace.value = p
  palaceVisible.value = true
}

const closePalace = () => {
  palaceVisible.value = false
  selectedPalace.value = null
}

const starText = (score?: number) => formatStar(score || 0)

const reQimen = () => {
  if (!detail.value) return
  qimenStore.setPrefillInput({
    datetime: detail.value.datetime,
    gender: detail.value.gender,
    type: detail.value.type
  })
  uni.switchTab({ url: '/pages/qimen-input/index' })
}

const confirmDelete = () => {
  if (!detail.value) return
  uni.showModal({
    title: '提示',
    content: '确定删除该记录吗？',
    success: async (res) => {
      if (!res.confirm) return
      try {
        await qimenStore.deleteHistoryRecord(detail.value.id)
        uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/history-list/index' }) })
      } catch {
        // request.ts 已统一toast
      }
    }
  })
}
</script>

<style scoped>
.history-detail-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f5f5f5;
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

.info-bar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 24rpx 30rpx;
  border-radius: 20rpx;
  margin-bottom: 24rpx;
  font-size: 26rpx;
  line-height: 1.6;
}

.plate-container {
  background: #fff;
  padding: 30rpx;
  border-radius: 20rpx;
  margin-bottom: 24rpx;
}

.result-section {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.fortune-item {
  margin-bottom: 20rpx;
}

.fortune-name {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 8rpx;
}

.fortune-stars {
  color: #ffd700;
  font-size: 28rpx;
}

.action-buttons {
  display: flex;
  gap: 20rpx;
}

.btn {
  flex: 1;
  height: 88rpx;
  border-radius: 44rpx;
  font-size: 30rpx;
  font-weight: 500;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.btn-danger {
  background: #fff;
  color: #e74c3c;
  border-width: 4rpx;
  border-style: solid;
  border-color: #e74c3c;
}

.loading {
  text-align: center;
  padding: 30rpx 0;
}

.loading-text {
  font-size: 26rpx;
  color: #999;
}
</style>

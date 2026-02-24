<!-- 文档引用：PROJECT_SPEC.md - 2.2.10节 -->
<!-- 页面10：万年历页 -->
<!-- UI模板参考：template/10-calendar.html -->

<template>
  <view class="calendar-page">
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">万年历</text>
    </view>

    <scroll-view class="content" scroll-y>
      <CalendarPicker
        :year="year"
        :month="month"
        :days="dayCells"
        @changeMonth="handleChangeMonth"
        @selectDay="handleSelectDay"
      />

      <view class="date-detail" v-if="selectedDay">
        <view class="detail-item">
          <text class="detail-icon">📅</text>
          <text class="detail-label">公历：</text>
          <text class="detail-value">{{ selectedDay.date }}</text>
        </view>
        <view class="detail-item">
          <text class="detail-icon">🏮</text>
          <text class="detail-label">农历：</text>
          <text class="detail-value">{{ selectedDay.lunar_date }}</text>
        </view>
        <view class="detail-item">
          <text class="detail-icon">🌿</text>
          <text class="detail-label">节气：</text>
          <text class="detail-value">{{ selectedDay.solar_term || '-' }}</text>
        </view>
        <view class="detail-item">
          <text class="detail-icon">🔮</text>
          <text class="detail-label">干支：</text>
          <text class="detail-value">{{ selectedDay.stem_branch }}</text>
        </view>
      </view>

      <view v-if="loading" class="loading">
        <text class="loading-text">加载中...</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import CalendarPicker from '@/modules/qimen/components/CalendarPicker.vue'
import { useQimenStore } from '@/modules/qimen/store/index'

const qimenStore = useQimenStore()

const now = new Date()
const year = ref(now.getFullYear())
const month = ref(now.getMonth() + 1)

const loading = ref(false)
const days = ref<any[]>([])
const selectedDay = ref<any | null>(null)

const fetchMonth = async () => {
  loading.value = true
  try {
    const res = await qimenStore.getCalendarData(year.value, month.value)
    days.value = res.days || []
    selectedDay.value = days.value.find(d => d.is_today) || days.value[0] || null
  } catch {
    days.value = []
    selectedDay.value = null
  } finally {
    loading.value = false
  }
}

onShow(fetchMonth)

const dayCells = computed(() => {
  return (days.value || []).map(d => ({
    day: d.day,
    isToday: !!d.is_today,
    isSelected: selectedDay.value?.date === d.date
  }))
})

const handleChangeMonth = (payload: { year: number; month: number }) => {
  year.value = payload.year
  month.value = payload.month
  fetchMonth()
}

const handleSelectDay = (payload: { day: number }) => {
  const d = (days.value || []).find(x => x.day === payload.day)
  if (d) selectedDay.value = d
}

const handleBack = () => {
  uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/qimen-input/index' }) })
}
</script>

<style scoped>
.calendar-page {
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

.date-detail {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-top: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
  font-size: 28rpx;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-icon {
  font-size: 36rpx;
  margin-right: 20rpx;
}

.detail-label {
  color: #666;
  margin-right: 16rpx;
}

.detail-value {
  color: #333;
  font-weight: 500;
  flex: 1;
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

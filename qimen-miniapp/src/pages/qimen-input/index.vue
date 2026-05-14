<!-- 文档引用：PROJECT_SPEC.md - 2.2.4节 -->
<!-- 页面4：起盘输入页 -->
<!-- UI模板参考：template/4-qipan-input.html -->

<template>
  <view class="qimen-input-page">
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">奇门起盘</text>
    </view>

    <!-- 未登录：显示与个人中心一致的“请先登录”卡片 -->
    <view v-if="!isLogin" class="not-login-wrapper">
      <view class="not-login-card">
        <view class="not-login-icon">👤</view>
        <text class="not-login-text">请先登录后再起盘</text>
        <button class="login-btn" @click="goLogin">立即登录</button>
      </view>
    </view>

    <!-- 已登录：显示起盘表单 -->
    <scroll-view v-else class="content" scroll-y>
      <view class="tip-box">💡 请输入准确的出生时间，以获得精准的起盘结果</view>

      <!-- 公历/农历切换 -->
      <view class="form-section">
        <view class="section-title">
          <text class="section-icon">📅</text>
          <text>公历/农历切换</text>
        </view>
        <view class="radio-group">
          <view class="radio-item" @click="calendarType = '公历'">
            <view class="radio-circle" :class="{ active: calendarType === '公历' }" />
            <text class="radio-label">公历</text>
          </view>
          <view class="radio-item" @click="calendarType = '农历'">
            <view class="radio-circle" :class="{ active: calendarType === '农历' }" />
            <text class="radio-label">农历</text>
          </view>
        </view>
      </view>

      <!-- 日期选择 -->
      <view class="form-section">
        <view class="section-title">
          <text class="section-icon">📅</text>
          <text>选择日期</text>
        </view>
        <picker mode="date" :value="date" start="1900-01-01" end="2100-12-31" @change="handleDateChange">
          <view class="select-box">
            <text class="select-value">{{ displayDate }}</text>
            <text class="select-arrow">▼</text>
          </view>
        </picker>
      </view>

      <!-- 时辰选择 -->
      <view class="form-section">
        <view class="section-title">
          <text class="section-icon">🕐</text>
          <text>选择时辰</text>
        </view>
        <picker mode="selector" :range="shichenDisplayList" :value="shichenIndex" @change="handleShichenChange">
          <view class="select-box">
            <text class="select-value">{{ displayShichen }}</text>
            <text class="select-arrow">▼</text>
          </view>
        </picker>
      </view>

      <!-- 性别选择 -->
      <view class="form-section">
        <view class="section-title">
          <text class="section-icon">👤</text>
          <text>性别</text>
        </view>
        <view class="radio-group">
          <view class="radio-item" @click="gender = '男'">
            <view class="radio-circle" :class="{ active: gender === '男' }" />
            <text class="radio-label">男</text>
          </view>
          <view class="radio-item" @click="gender = '女'">
            <view class="radio-circle" :class="{ active: gender === '女' }" />
            <text class="radio-label">女</text>
          </view>
        </view>
      </view>

      <!-- 起盘类型 -->
      <view class="form-section">
        <view class="section-title">
          <text class="section-icon">🔮</text>
          <text>起盘类型</text>
        </view>
        <view class="radio-group">
          <view class="radio-item">
            <view class="radio-circle active" />
            <text class="radio-label">时家奇门</text>
          </view>
          <view class="radio-item disabled">
            <view class="radio-circle" />
            <text class="radio-label disabled-text">日家奇门</text>
          </view>
        </view>
      </view>

      <button class="start-btn" @click="handleStart">开始起盘</button>

      <view class="quick-link" @click="goCalendar">📅 万年历查询</view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/modules/user/store/index'
import { useQimenStore } from '@/modules/qimen/store/index'
import { SHICHEN_LIST } from '@/common/utils/constants'

const userStore = useUserStore()
const qimenStore = useQimenStore()
const isLogin = computed(() => userStore.loggedIn)

const calendarType = ref<'公历' | '农历'>('公历')
const date = ref('')
const shichenIndex = ref(0)
const gender = ref<'男' | '女'>('男')

const shichenDisplayList = computed(() => SHICHEN_LIST.map(s => `${s.label}(${s.range})`))
const selectedShichen = computed(() => SHICHEN_LIST[shichenIndex.value])

const displayDate = computed(() => date.value || '请选择日期')
const displayShichen = computed(() => {
  const s = selectedShichen.value
  return `${s.label}(${s.range})`
})

const goLogin = () => {
  uni.navigateTo({
    url: `/pages/login/index?redirect=${encodeURIComponent('/pages/qimen-input/index')}`
  })
}

const handleBack = () => {
  // 兼容 tabbar 根页：如果没有可返回的历史，则回到首页 tab
  try {
    // H5 / 小程序环境均支持 getCurrentPages
    // eslint-disable-next-line no-undef
    const pages = getCurrentPages && getCurrentPages()
    const len = Array.isArray(pages) ? pages.length : 0
    if (!len || len <= 1) {
      uni.switchTab({ url: '/pages/index/index' })
      return
    }
  } catch {
    // ignore，走兜底逻辑
  }
  uni.navigateBack({
    fail() {
      uni.switchTab({ url: '/pages/index/index' })
    }
  })
}

const handleDateChange = (e: any) => {
  date.value = e.detail.value
}

const handleShichenChange = (e: any) => {
  shichenIndex.value = Number(e.detail.value || 0)
}

const goCalendar = () => {
  uni.navigateTo({ url: '/pages/calendar/index' })
}

const handleStart = async () => {
  if (!date.value) return uni.showToast({ title: '请选择日期', icon: 'none' })
  if (!gender.value) return uni.showToast({ title: '请选择性别', icon: 'none' })

  const y = Number(date.value.split('-')[0])
  if (y < 1900 || y > 2100) return uni.showToast({ title: '日期范围必须在1900-2100年之间', icon: 'none' })

  const startTime = selectedShichen.value.range.split('-')[0] // 如 23:00
  const datetime = `${date.value} ${startTime}`

  // 不能超过当前时间（与后端一致）
  const dt = new Date(datetime.replace(' ', 'T') + ':00')
  if (dt.getTime() > Date.now()) return uni.showToast({ title: '日期不能超过当前时间', icon: 'none' })

  try {
    await qimenStore.calculateQimen({
      datetime,
      gender: gender.value,
      type: '时家奇门',
      calendar_type: calendarType.value
    })
    uni.navigateTo({ url: '/pages/qimen-plate/index' })
  } catch {
    // request.ts 已统一toast
  }
}

onShow(() => {
  if (!isLogin.value) {
    // 未登录时仅展示“请先登录”提示，不自动跳转
    return
  }

  // 从历史详情页“重新起盘”带入参数
  if (qimenStore.prefillInput && qimenStore.prefillInput.datetime) {
    const dt: string = qimenStore.prefillInput.datetime
    const parts = dt.split(' ')
    if (parts[0]) {
      date.value = parts[0]
    }
    if (qimenStore.prefillInput.gender === '男' || qimenStore.prefillInput.gender === '女') {
      gender.value = qimenStore.prefillInput.gender
    }
    calendarType.value = '公历'
    qimenStore.clearPrefillInput()
  }
})
</script>

<style scoped>
.qimen-input-page {
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

.tip-box {
  background: #e7f3ff;
  border-left: 8rpx solid #409eff;
  padding: 24rpx 30rpx;
  margin-bottom: 30rpx;
  border-radius: 8rpx;
  font-size: 26rpx;
  color: #409eff;
  line-height: 1.6;
}

.form-section {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
}

.section-icon {
  margin-right: 12rpx;
  font-size: 30rpx;
}

.radio-group {
  display: flex;
  gap: 40rpx;
}

.radio-item {
  display: flex;
  align-items: center;
}

.radio-item.disabled {
  opacity: 0.5;
}

.radio-circle {
  width: 32rpx;
  height: 32rpx;
  border-radius: 16rpx;
  border-width: 4rpx;
  border-style: solid;
  border-color: #ddd;
  margin-right: 12rpx;
  position: relative;
}

.radio-circle.active {
  border-color: #667eea;
}

.radio-circle.active::after {
  content: '';
  position: absolute;
  width: 18rpx;
  height: 18rpx;
  border-radius: 9rpx;
  background: #667eea;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.radio-label {
  font-size: 28rpx;
  color: #333;
}

.disabled-text {
  color: #ccc;
}

.select-box {
  background: #f8f8f8;
  border-radius: 16rpx;
  padding: 24rpx 30rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.select-value {
  font-size: 28rpx;
  color: #333;
}

.select-arrow {
  color: #999;
  font-size: 26rpx;
}

.start-btn {
  width: 100%;
  height: 100rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 50rpx;
  font-size: 32rpx;
  font-weight: bold;
  margin-top: 20rpx;
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.4);
}

.quick-link {
  margin-top: 24rpx;
  text-align: center;
  color: #667eea;
  font-size: 28rpx;
  padding: 20rpx 0;
}
</style>

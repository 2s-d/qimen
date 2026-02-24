<!-- 文档引用：PROJECT_SPEC.md - 2.2.1节 -->
<!-- 页面1：首页/引导页 -->
<!-- UI模板参考：template/1.html -->

<template>
  <view class="container">
    <!-- 顶部区域（高度120rpx） -->
    <view class="header">
      <view class="logo">🔮</view>
      <text class="app-title">{{ appName }}</text>
    </view>

    <!-- 轮播图区域（高度300rpx） -->
    <swiper 
      class="banner" 
      :indicator-dots="banners.length > 1" 
      :autoplay="banners.length > 1" 
      :interval="3000" 
      :duration="500"
      :circular="banners.length > 1"
      indicator-color="rgba(255, 255, 255, 0.5)"
      indicator-active-color="#ffffff"
      @change="handleBannerChange"
    >
      <swiper-item v-for="(banner, index) in banners" :key="index" @click="handleBannerClick(banner)">
        <image 
          class="banner-item" 
          :src="banner.url || '/static/logo.png'" 
          mode="aspectFill"
          @error="handleBannerImageError"
        />
      </swiper-item>
    </swiper>

    <!-- 今日运势卡片（高度200rpx） -->
    <view class="fortune-card">
      <view class="fortune-header">
        <text class="fortune-icon">📅</text>
        <text class="fortune-title">今日运势</text>
      </view>
      <!-- 加载中状态 -->
      <view v-if="fortuneLoading" class="fortune-loading">
        <text class="loading-text">加载中...</text>
      </view>
      <!-- 错误状态 -->
      <view v-else-if="fortuneError" class="fortune-error">
        <text class="error-text">加载失败，请稍后重试</text>
        <button class="retry-btn" @click="retryLoadFortune">重试</button>
      </view>
      <!-- 正常显示 -->
      <view v-else-if="dailyFortune" class="fortune-content">
        <view class="fortune-rating">{{ formatStar(dailyFortune.overall_score) }} {{ dailyFortune.overall_score }}分</view>
        <view class="fortune-desc">{{ dailyFortune.overall_fortune }} {{ getFortuneSummary() }}</view>
        <button class="fortune-btn" @click="handleViewFortuneDetail">查看详情 →</button>
      </view>
      <!-- 空数据状态 -->
      <view v-else class="fortune-empty">
        <text class="empty-text">暂无运势数据</text>
      </view>
    </view>

    <!-- 功能宫格区域（2行3列） -->
    <view class="function-grid">
      <view class="grid-container">
        <view class="grid-item" @click="handleFunctionClick('qimen-input')">
          <view class="grid-icon">🔮</view>
          <text class="grid-label">起盘</text>
        </view>
        <view class="grid-item" @click="handleFunctionClick('history-list')">
          <view class="grid-icon">📜</view>
          <text class="grid-label">历史</text>
        </view>
        <view class="grid-item" @click="handleFunctionClick('knowledge')">
          <view class="grid-icon">📚</view>
          <text class="grid-label">知识</text>
        </view>
        <view class="grid-item" @click="handleFunctionClick('calendar')">
          <view class="grid-icon">📅</view>
          <text class="grid-label">万年历</text>
        </view>
        <view class="grid-item" @click="handleFunctionClick('about')">
          <view class="grid-icon">ℹ️</view>
          <text class="grid-label">关于</text>
        </view>
        <view class="grid-item" @click="handleFunctionClick('more')">
          <view class="grid-icon">⚙️</view>
          <text class="grid-label">更多</text>
        </view>
      </view>
    </view>

    <!-- 公告滚动区域（高度80rpx） -->
    <view class="announcement" v-if="announcements.length > 0 || loading" @click="handleAnnouncementClick">
      <text class="announcement-icon">📢</text>
      <view class="announcement-text-wrapper">
        <view v-if="loading && announcements.length === 0" class="announcement-loading">
          <text class="loading-text">加载中...</text>
        </view>
        <view v-else-if="announcements.length > 0" class="announcement-scroll-container">
          <text 
            class="announcement-text" 
            :class="{ 'announcement-scroll': announcements.length > 1 }"
          >
            {{ getAnnouncementText() }}
          </text>
          <!-- 如果只有一条公告，也显示滚动效果（从右向左） -->
          <text 
            v-if="announcements.length === 1" 
            class="announcement-text announcement-scroll-duplicate"
          >
            {{ getAnnouncementText() }}
          </text>
        </view>
        <view v-else class="announcement-empty">
          <text class="empty-text">暂无公告</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
// 文档引用：PROJECT_SPEC.md - 2.2.1节
import { ref, onMounted, computed } from 'vue'
import { useSystemStore } from '@/store/index'
import { useQimenStore } from '@/store/index'
import { useUserStore } from '@/store/index'
import { formatStar } from '@/common/utils/format'
import { checkLogin } from '@/modules/user/utils/auth'

const systemStore = useSystemStore()
const qimenStore = useQimenStore()
const userStore = useUserStore()

const appName = computed(() => systemStore.getAppName)
const banners = computed(() => {
  const bannerList = systemStore.getBannerImages
  // 如果banners为空，显示默认图片
  if (!bannerList || bannerList.length === 0) {
    return [{ url: '/static/logo.png', link: '' }]
  }
  return bannerList
})
const announcements = computed(() => systemStore.getAnnouncementsList)
const dailyFortune = computed(() => qimenStore.dailyFortune)

// 加载状态
const loading = ref(true)
const fortuneLoading = ref(true)
const configError = ref(false)
const announcementError = ref(false)
const fortuneError = ref(false)

// 页面加载时调用API（文档引用：PROJECT_SPEC.md - 145-149行）
onMounted(async () => {
  loading.value = true
  try {
    // 并行调用3个API
    await Promise.allSettled([
      systemStore.getSystemConfig().catch(err => {
        configError.value = true
        console.error('获取系统配置失败:', err)
        uni.showToast({ title: '加载配置失败', icon: 'none', duration: 2000 })
        throw err
      }),
      systemStore.getAnnouncements().catch(err => {
        announcementError.value = true
        console.error('获取公告失败:', err)
        // 公告失败不显示toast，因为不是关键功能
        throw err
      }),
      qimenStore.getDailyFortune().catch(err => {
        fortuneError.value = true
        fortuneLoading.value = false
        console.error('获取今日运势失败:', err)
        uni.showToast({ title: '加载运势失败', icon: 'none', duration: 2000 })
        throw err
      })
    ])
  } catch (error) {
    console.error('加载首页数据失败:', error)
  } finally {
    loading.value = false
    fortuneLoading.value = false
  }
})

// 轮播图切换（文档引用：PROJECT_SPEC.md - 150-154行）
const handleBannerChange = (e: any) => {
  // 可以在这里处理轮播图切换逻辑
}

// 轮播图点击（预留功能）
const handleBannerClick = (banner: any) => {
  if (banner.link) {
    // 预留功能：点击图片可跳转
    uni.navigateTo({ url: banner.link })
  }
}

// 轮播图图片加载失败处理
const handleBannerImageError = (e: any) => {
  console.error('轮播图加载失败:', e)
  // 使用默认图片
}

// 今日运势卡片 - 获取运势简述（文档引用：PROJECT_SPEC.md - 155-157行）
const getFortuneSummary = (): string => {
  if (!dailyFortune.value) return ''
  // 从fortunes中取一个运势简述，或使用overall_fortune
  const fortunes = dailyFortune.value.fortunes
  if (fortunes && fortunes.career) {
    return fortunes.career.text.substring(0, 30) + '...'
  }
  return dailyFortune.value.overall_fortune || ''
}

// 查看今日运势详情（文档引用：PROJECT_SPEC.md - 157行）
const handleViewFortuneDetail = () => {
  // 跳转到解读结果页（今日运势模式）
  uni.navigateTo({
    url: '/pages/qimen-result/index?mode=fortune'
  })
}

// 功能宫格点击（文档引用：PROJECT_SPEC.md - 158-165行）
const handleFunctionClick = (type: string) => {
  switch (type) {
    case 'qimen-input':
      uni.switchTab({ url: '/pages/qimen-input/index' })
      break
    case 'history-list':
      uni.switchTab({ url: '/pages/history-list/index' })
      break
    case 'knowledge':
      uni.navigateTo({ url: '/pages/knowledge/index' })
      break
    case 'calendar':
      uni.navigateTo({ url: '/pages/calendar/index' })
      break
    case 'about':
      uni.navigateTo({ url: '/pages/about/index' })
      break
    case 'more':
      // 暂无功能（预留）
      uni.showToast({ title: '功能开发中', icon: 'none' })
      break
  }
}

// 获取公告文字（文档引用：PROJECT_SPEC.md - 166-169行）
const getAnnouncementText = (): string => {
  if (announcements.value.length === 0) return ''
  // 最多显示最新3条，超过3条轮播显示（文档引用：PROJECT_SPEC.md - 179行）
  const displayAnnouncements = announcements.value.slice(0, 3)
  return displayAnnouncements.map(a => a.title).join(' | ')
}

// 重试加载今日运势
const retryLoadFortune = async () => {
  fortuneLoading.value = true
  fortuneError.value = false
  try {
    await qimenStore.getDailyFortune()
    fortuneError.value = false
  } catch (error) {
    fortuneError.value = true
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    fortuneLoading.value = false
  }
}

// 公告点击（文档引用：PROJECT_SPEC.md - 169行）
const handleAnnouncementClick = () => {
  if (announcements.value.length === 0) return
  const firstAnnouncement = announcements.value[0]
  uni.showModal({
    title: firstAnnouncement.title,
    content: firstAnnouncement.content,
    showCancel: false
  })
}
</script>

<style scoped>
/* 文档引用：template/1.html - 样式参考 */

.container {
  width: 100%;
  background: #f5f5f5;
  min-height: 100vh;
  padding-bottom: 100rpx; /* 为底部TabBar留出空间（uni-app原生TabBar高度100rpx） */
}

/* 顶部区域（高度120rpx = 60px） */
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20rpx 30rpx;
  display: flex;
  align-items: center;
  height: 120rpx;
}

.logo {
  width: 80rpx;
  height: 80rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40rpx;
  margin-right: 24rpx;
}

.app-title {
  font-size: 36rpx;
  font-weight: bold;
}

/* 轮播图区域（高度300rpx = 150px） */
.banner {
  height: 300rpx;
  width: 100%;
}

.banner-item {
  width: 100%;
  height: 100%;
}

/* 今日运势卡片（高度约200rpx = 100px） */
.fortune-card {
  margin: 30rpx;
  background: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
}

.fortune-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.fortune-icon {
  font-size: 40rpx;
  margin-right: 16rpx;
}

.fortune-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.fortune-rating {
  color: #ffd700;
  font-size: 32rpx;
  margin-bottom: 12rpx;
}

.fortune-desc {
  color: #666;
  font-size: 26rpx;
  margin-bottom: 24rpx;
  line-height: 1.5;
}

.fortune-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 16rpx 32rpx;
  border-radius: 32rpx;
  font-size: 26rpx;
}

/* 今日运势卡片 - 加载/错误/空状态 */
.fortune-loading,
.fortune-error,
.fortune-empty {
  padding: 40rpx 0;
  text-align: center;
}

.loading-text,
.error-text,
.empty-text {
  font-size: 26rpx;
  color: #999;
}

.retry-btn {
  margin-top: 20rpx;
  padding: 12rpx 24rpx;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 20rpx;
  font-size: 24rpx;
}

.fortune-content {
  width: 100%;
}

/* 功能宫格 */
.function-grid {
  margin: 0 30rpx 30rpx;
  background: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30rpx;
}

.grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20rpx 0;
}

.grid-icon {
  width: 90rpx;
  height: 90rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 44rpx;
  margin-bottom: 12rpx;
}

.grid-label {
  font-size: 26rpx;
  color: #333;
}

/* 公告滚动区域（高度80rpx = 40px） */
.announcement {
  margin: 0 30rpx 30rpx;
  background: #fff3cd;
  border-radius: 12rpx;
  padding: 20rpx 24rpx;
  display: flex;
  align-items: center;
  overflow: hidden;
  height: 80rpx;
}

.announcement-icon {
  font-size: 32rpx;
  margin-right: 16rpx;
  flex-shrink: 0;
}

.announcement-text-wrapper {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.announcement-loading,
.announcement-empty {
  display: flex;
  align-items: center;
  height: 100%;
}

.announcement-scroll-container {
  display: flex;
  align-items: center;
  height: 100%;
  overflow: hidden;
}

.announcement-text {
  font-size: 26rpx;
  color: #856404;
  white-space: nowrap;
  flex-shrink: 0;
}

/* 公告滚动动画（从右向左无限滚动） */
.announcement-scroll {
  animation: scroll-left 20s linear infinite;
  display: inline-block;
}

.announcement-scroll-duplicate {
  animation: scroll-left 20s linear infinite;
  margin-left: 100rpx; /* 两条文字之间的间距 */
}

@keyframes scroll-left {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-100%);
  }
}
</style>

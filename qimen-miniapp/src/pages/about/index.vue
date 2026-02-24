<!-- 文档引用：PROJECT_SPEC.md - 2.2.12节 -->
<!-- 页面12：关于/帮助页 -->
<!-- UI模板参考：template/12-about.html -->

<template>
  <view class="about-page">
    <!-- 自定义导航栏（navigationStyle: custom） -->
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">关于</text>
    </view>

    <scroll-view class="content" scroll-y>
      <!-- 应用信息区域 -->
      <view class="app-info">
        <view class="app-logo">🔮</view>
        <text class="app-name">奇门遁甲算命小程序</text>
        <text class="app-version">版本号：v{{ appVersion }}</text>
      </view>

      <!-- 应用介绍 -->
      <view class="section intro-section">
        <view class="section-title">应用介绍</view>
        <view class="section-content">{{ aboutText }}</view>
      </view>

      <!-- 使用帮助（可折叠） -->
      <view class="section help-section">
        <view class="section-title">使用帮助</view>
        <view v-if="helpLoading" class="help-loading">
          <text class="loading-text">加载中...</text>
        </view>
        <HelpAccordion v-else :questions="helpQuestions" />
      </view>

      <!-- 联系我们 -->
      <view class="section contact-section">
        <view class="section-title">联系我们</view>
        <view class="contact-info">
          <view class="contact-left">
            <text class="contact-icon">📧</text>
            <text class="email">{{ contactEmail }}</text>
          </view>
          <view class="copy-btn" @click="handleCopyEmail">点击复制</view>
        </view>
      </view>

      <!-- 免责声明（必须展示） -->
      <view class="section disclaimer-section">
        <view class="section-title">免责声明</view>
        <view class="section-content">{{ disclaimerText }}</view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSystemStore } from '@/modules/system/store/index'
import HelpAccordion from '@/modules/system/components/HelpAccordion.vue'

const systemStore = useSystemStore()
const helpLoading = ref(false)

// 从config提取版本号（支持对象或字符串）
const appVersion = computed(() => {
  const v = systemStore.config?.app_version
  if (typeof v === 'object' && v?.version) return v.version
  return v || '1.0.0'
})

const aboutText = computed(() => systemStore.getAboutText)
const contactEmail = computed(() => {
  const e = systemStore.config?.contact_email
  if (typeof e === 'object' && e?.email) return e.email
  return e || 'contact@example.com'
})
const disclaimerText = computed(() => systemStore.getDisclaimer)
const helpQuestions = computed(() => systemStore.helpDoc?.questions || [])

const handleBack = () => {
  uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/index/index' }) })
}

const handleCopyEmail = () => {
  uni.setClipboardData({
    data: contactEmail.value,
    success: () => uni.showToast({ title: '已复制到剪贴板', icon: 'success' }),
    fail: () => uni.showToast({ title: '复制失败', icon: 'none' })
  })
}

onMounted(async () => {
  // 确保配置已加载（首页可能已加载）
  if (!systemStore.config) {
    try {
      await systemStore.getSystemConfig()
    } catch {
      // 使用store默认值
    }
  }
  // 加载帮助文档
  helpLoading.value = true
  try {
    await systemStore.getHelpDoc()
  } catch {
    // 使用空列表，HelpAccordion会显示空
  } finally {
    helpLoading.value = false
  }
})
</script>

<style scoped>
.about-page {
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
  padding-bottom: 0;
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
  padding: 40rpx 30rpx 80rpx;
  height: 0;
}

.app-info {
  text-align: center;
  margin-bottom: 40rpx;
}

.app-logo {
  width: 160rpx;
  height: 160rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 80rpx;
  margin: 0 auto 30rpx;
}

.app-name {
  display: block;
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 16rpx;
}

.app-version {
  font-size: 26rpx;
  color: #999;
}

.section {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 24rpx;
}

.section-content {
  font-size: 26rpx;
  color: #666;
  line-height: 1.8;
}

.help-section {
  min-height: 120rpx;
}

.help-loading {
  padding: 20rpx 0;
  text-align: center;
}

.loading-text {
  font-size: 26rpx;
  color: #999;
}

.contact-section {
  min-height: 70rpx;
}

.contact-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.contact-left {
  display: flex;
  align-items: center;
}

.contact-icon {
  font-size: 32rpx;
  margin-right: 16rpx;
}

.email {
  font-size: 26rpx;
  color: #667eea;
}

.copy-btn {
  background: #667eea;
  color: #fff;
  padding: 12rpx 24rpx;
  border-radius: 8rpx;
  font-size: 24rpx;
}

.disclaimer-section {
  min-height: 100rpx;
}
</style>

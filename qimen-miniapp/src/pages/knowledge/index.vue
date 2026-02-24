<!-- 文档引用：PROJECT_SPEC.md - 2.2.11节 -->
<!-- 页面11：基础知识页 -->
<!-- UI模板参考：template/11-knowledge.html -->

<template>
  <view class="knowledge-page">
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">基础知识</text>
    </view>

    <scroll-view class="content" scroll-y @refresherrefresh="refresh" refresher-enabled :refresher-triggered="refreshing">
      <!-- 顶部分类导航，按照模板做成一行横向标签栏 -->
      <view class="tabs">
        <view
          v-for="t in tabs"
          :key="t.value"
          class="tab"
          :class="{ active: activeTab === t.value }"
          @click="selectTab(t.value)"
        >
          {{ t.label }}
        </view>
      </view>

      <view class="article-list" v-if="articles.length > 0">
        <ArticleCard v-for="a in articles" :key="a.id" :article="a" />
      </view>

      <view v-else class="empty">
        <text class="empty-text">暂无内容</text>
      </view>

      <view v-if="loading" class="loading">
        <text class="loading-text">加载中...</text>
      </view>
    </scroll-view>

    <!-- 问小奇悬浮按钮（右侧上半区：约 1/3 屏高） -->
    <view class="ask-xiaoqi" @click="goAskXiaoqi">
      <view class="ask-btn">
        <image class="ask-icon" src="/static/icons/ask-chat.svg" mode="aspectFit" />
      </view>
      <text class="ask-label">问小奇</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useQimenStore } from '@/modules/qimen/store/index'
import ArticleCard from '@/modules/qimen/components/ArticleCard.vue'

const qimenStore = useQimenStore()

const tabs = [
  { label: '入门', value: '入门' },
  { label: '八门', value: '八门' },
  { label: '九星', value: '九星' },
  { label: '八神', value: '八神' },
  { label: '应用', value: '应用' }
]

const activeTab = ref<string>('入门')
const loading = ref(false)
const refreshing = ref(false)

const articles = computed(() => qimenStore.knowledgeArticles || [])

const fetchArticles = async () => {
  loading.value = true
  try {
    await qimenStore.getKnowledgeArticles(activeTab.value)
  } catch {
    // request.ts 已统一toast
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

onShow(fetchArticles)

const selectTab = (v: string) => {
  if (activeTab.value === v) return
  activeTab.value = v
  fetchArticles()
}

const refresh = async () => {
  refreshing.value = true
  await fetchArticles()
}

const handleBack = () => {
  uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/index/index' }) })
}

const goAskXiaoqi = () => {
  uni.navigateTo({ url: '/pages/ai-chat/index' })
}
</script>

<style scoped>
.knowledge-page {
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

.tabs {
  display: flex;
  background: #fff;
  border-radius: 20rpx;
  padding: 20rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
  white-space: nowrap;
}

.tab {
  padding: 16rpx 28rpx;
  border-radius: 12rpx;
  font-size: 28rpx;
  color: #666;
  margin-right: 16rpx;
}

.tab:last-child {
  margin-right: 0;
}

.tab.active {
  background: linear-gradient(200deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.empty {
  text-align: center;
  padding: 120rpx 40rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #999;
}

.loading {
  text-align: center;
  padding: 30rpx 0;
}

.loading-text {
  font-size: 26rpx;
  color: #999;
}

.ask-xiaoqi {
  position: fixed;
  right: 24rpx;
  top: 36%;
  transform: translateY(-50%);
  z-index: 999;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ask-btn {
  width: 104rpx;
  height: 104rpx;
  border-radius: 52rpx;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6rpx 16rpx rgba(0, 0, 0, 0.15);
}

.ask-icon {
  width: 68rpx;
  height: 68rpx;
}

.ask-label {
  margin-top: 8rpx;
  font-size: 22rpx;
  color: #667eea;
}
</style>

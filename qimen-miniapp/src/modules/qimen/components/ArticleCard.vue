<!-- 文档引用：PROJECT_SPEC.md - 1423行 -->
<!-- 知识文章卡片组件 -->

<template>
  <view class="article-card">
    <view class="article-header">
      <text class="article-icon">📖</text>
      <text class="article-title">{{ article.title }}</text>
    </view>
    <view class="article-preview" v-if="!expanded">
      {{ article.summary || article.preview }}
    </view>
    <view v-else class="article-content">
      <rich-text :nodes="article.content || article.summary"></rich-text>
    </view>
    <view class="read-more" @click="toggle">
      <text>{{ expanded ? '收起' : '阅读全文' }}</text>
      <text class="read-more-icon">{{ expanded ? '▲' : '▼' }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  article: any
}>()

const expanded = ref(false)

const toggle = () => {
  expanded.value = !expanded.value
}
</script>

<style scoped>
.article-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.article-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.article-icon {
  font-size: 40rpx;
  margin-right: 16rpx;
}

.article-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.article-preview,
.article-content {
  font-size: 26rpx;
  color: #666;
  line-height: 1.8;
  margin-bottom: 16rpx;
}

.read-more {
  color: #667eea;
  font-size: 26rpx;
  display: inline-flex;
  align-items: center;
}

.read-more-icon {
  margin-left: 8rpx;
}
</style>


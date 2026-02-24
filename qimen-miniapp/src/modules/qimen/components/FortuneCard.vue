<!-- 文档引用：PROJECT_SPEC.md - 1420行 -->
<!-- 运势卡片组件 -->

<template>
  <view class="fortune-card">
    <view class="fortune-header">
      <text class="fortune-icon">{{ icon }}</text>
      <text class="fortune-name">{{ title }}</text>
    </view>
    <view class="fortune-stars">{{ stars }}</view>
    <view class="fortune-desc">{{ desc }}</view>
  </view>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  icon: string
  stars: string
  desc: string
}>()
</script>

<style scoped>
.fortune-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 24rpx;
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

.fortune-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.fortune-stars {
  color: #ffd700;
  font-size: 30rpx;
  margin-bottom: 12rpx;
}

.fortune-desc {
  font-size: 26rpx;
  color: #666;
  line-height: 1.8;
}
</style>


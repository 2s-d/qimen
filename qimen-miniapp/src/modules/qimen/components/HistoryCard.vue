<!-- 文档引用：PROJECT_SPEC.md - 1421行 -->
<!-- 历史记录卡片组件 -->

<template>
  <view class="record-card">
    <view class="record-time">📅 {{ record.display_time }}</view>
    <view class="record-info">
      <text>👤 {{ record.gender_text || record.gender }}</text>
      <text class="divider">|</text>
      <text>🔮 {{ record.type_text || record.type }}</text>
    </view>
    <view class="record-fortune">运势：{{ record.fortune_text || record.score_text || '--' }}</view>
    <view class="record-actions">
      <button class="btn-small btn-view" @click.stop="emit('view', record)">查看详情</button>
      <button class="btn-small btn-delete" @click.stop="emit('delete', record)">删除</button>
    </view>
  </view>
</template>

<script setup lang="ts">
const props = defineProps<{
  record: any
}>()

const emit = defineEmits<{
  (e: 'view', record: any): void
  (e: 'delete', record: any): void
}>()
</script>

<style scoped>
.record-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
}

.record-time {
  font-size: 30rpx;
  color: #333;
  font-weight: 500;
  margin-bottom: 12rpx;
}

.record-info {
  font-size: 26rpx;
  color: #666;
  margin-bottom: 8rpx;
}

.divider {
  margin: 0 10rpx;
}

.record-fortune {
  font-size: 26rpx;
  color: #ffd700;
  margin-bottom: 20rpx;
}

.record-actions {
  display: flex;
  gap: 20rpx;
}

.btn-small {
  flex: 1;
  height: 64rpx;
  border-radius: 32rpx;
  border: none;
  font-size: 26rpx;
}

.btn-view {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.btn-delete {
  background: #fff;
  color: #e74c3c;
  border-width: 2rpx;
  border-style: solid;
  border-color: #e74c3c;
}
</style>


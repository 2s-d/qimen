<!-- 文档引用：PROJECT_SPEC.md - 1269行 -->
<!-- 用户信息卡片组件 -->

<template>
  <view class="user-card">
    <view class="user-info">
      <view class="avatar">👤</view>
      <view class="user-details">
        <text class="nickname">{{ displayNickname }}</text>
        <text class="username">账号：{{ userInfo?.username || '-' }}</text>
      </view>
    </view>
    <view class="stats">起盘次数：{{ (userInfo?.qimen_count ?? 0) }}次</view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  userInfo: any
}>()

const displayNickname = computed(() => {
  const n = props.userInfo?.nickname
  if (n && String(n).trim()) return n
  return '未设置昵称'
})
</script>

<style scoped>
.user-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 40rpx;
  color: #fff;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 30rpx;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60rpx;
  margin-right: 30rpx;
}

.user-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.nickname {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 10rpx;
}

.username {
  font-size: 26rpx;
  opacity: 0.9;
}

.stats {
  font-size: 26rpx;
  opacity: 0.9;
}
</style>


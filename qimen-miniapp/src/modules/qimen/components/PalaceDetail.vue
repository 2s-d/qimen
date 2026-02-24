<!-- 文档引用：PROJECT_SPEC.md - 1419行 -->
<!-- 宫位详情弹窗组件 -->

<template>
  <view v-if="visible" class="overlay" @click.self="close">
    <view class="modal">
      <view class="header">
        <text class="title">{{ palace?.position || '宫位详情' }}</text>
        <text class="close" @click="close">×</text>
      </view>
      <view class="body" v-if="palace">
        <view class="row">
          <text class="label">方位：</text>
          <text class="value">{{ palace.direction || '-' }}</text>
        </view>
        <view class="row">
          <text class="label">天盘星：</text>
          <text class="value">{{ palace.heaven_star || '-' }}</text>
        </view>
        <view class="row">
          <text class="label">地盘宫：</text>
          <text class="value">{{ palace.earth_palace || '-' }}</text>
        </view>
        <view class="row">
          <text class="label">人盘门：</text>
          <text class="value">{{ palace.human_door || '-' }}</text>
        </view>
        <view class="row">
          <text class="label">神盘：</text>
          <text class="value">{{ palace.god || '-' }}</text>
        </view>
        <view class="row">
          <text class="label">干支：</text>
          <text class="value">{{ palace.stem || '-' }} {{ palace.branch || '' }}</text>
        </view>
        <view class="row">
          <text class="label">吉凶：</text>
          <text class="value">{{ palace.fortune || '-' }}</text>
        </view>
        <view class="desc">
          <text class="desc-text">{{ palace.description || '暂无详细说明' }}</text>
        </view>
      </view>
      <view class="footer">
        <view class="btn" @click="close">关闭</view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
const props = defineProps<{
  visible: boolean
  palace: any | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const close = () => {
  emit('close')
}
</script>

<style scoped>
.overlay {
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal {
  width: 650rpx;
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.close {
  font-size: 36rpx;
  color: #999;
}

.body {
  margin-bottom: 20rpx;
}

.row {
  display: flex;
  margin-bottom: 10rpx;
  font-size: 26rpx;
}

.label {
  width: 140rpx;
  color: #666;
}

.value {
  flex: 1;
  color: #333;
}

.desc {
  margin-top: 10rpx;
}

.desc-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.8;
}

.footer {
  display: flex;
  justify-content: center;
}

.btn {
  width: 100%;
  height: 80rpx;
  border-radius: 40rpx;
  background: #667eea;
  color: #fff;
  text-align: center;
  line-height: 80rpx;
  font-size: 30rpx;
}
</style>


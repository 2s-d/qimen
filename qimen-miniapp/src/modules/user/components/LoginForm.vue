<!-- 文档引用：PROJECT_SPEC.md - 1270行 -->
<!-- 登录表单组件 -->

<template>
  <view class="content">
    <view class="logo-large">🔮</view>
    <view class="app-name">奇门遁甲</view>

    <view class="form-group">
      <view class="input-wrapper">
        <text class="input-icon">📱</text>
        <input
          v-model="username"
          class="input-field"
          type="text"
          placeholder="请输入账号"
          placeholder-class="placeholder"
        />
      </view>
    </view>

    <view class="form-group">
      <view class="input-wrapper">
        <text class="input-icon">🔒</text>
        <input
          v-model="password"
          class="input-field"
          :password="!showPassword"
          placeholder="请输入密码"
          placeholder-class="placeholder"
        />
        <text class="toggle-password" @click.stop="showPassword = !showPassword">👁</text>
      </view>
    </view>

    <button class="login-btn" @click="handleSubmit">登录</button>

    <view class="bottom-links">
      <text class="link" @click="emit('forgot')">忘记密码？</text>
      <text class="divider">|</text>
      <text class="link" @click="emit('register')">立即注册</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'submit', payload: { username: string; password: string }): void
  (e: 'register'): void
  (e: 'forgot'): void
}>()

const username = ref('')
const password = ref('')
const showPassword = ref(false)

const handleSubmit = () => {
  emit('submit', { username: username.value, password: password.value })
}
</script>

<style scoped>
.content {
  padding: 120rpx 60rpx 80rpx;
  text-align: center;
}

.logo-large {
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
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 100rpx;
}

.form-group {
  margin-bottom: 40rpx;
  text-align: left;
}

.input-wrapper {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
  height: 100rpx;
}

.input-icon {
  font-size: 40rpx;
  margin-right: 24rpx;
}

.input-field {
  flex: 1;
  font-size: 30rpx;
  color: #333;
}

.placeholder {
  color: #999;
}

.toggle-password {
  font-size: 36rpx;
  color: #999;
}

.login-btn {
  width: 100%;
  height: 100rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 50rpx;
  font-size: 32rpx;
  font-weight: bold;
  margin-top: 60rpx;
  box-shadow: 0 8rpx 24rpx rgba(102, 126, 234, 0.4);
}

.bottom-links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 40rpx;
  font-size: 28rpx;
  height: 80rpx;
}

.link {
  color: #667eea;
}

.divider {
  color: #ccc;
}
</style>


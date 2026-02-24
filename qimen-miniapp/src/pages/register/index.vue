<!-- 文档引用：PROJECT_SPEC.md - 2.2.3节 -->
<!-- 页面3：注册页 -->
<!-- UI模板参考：template/3-register.html -->

<template>
  <view class="register-page">
    <!-- 自定义导航栏（navigationStyle: custom） -->
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">注册</text>
    </view>

    <view class="content">
      <view class="form-group">
        <view class="input-wrapper">
          <text class="input-icon">👤</text>
          <input
            v-model="username"
            class="input-field"
            type="text"
            placeholder="3-20位，字母数字下划线"
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
            placeholder="6-20位密码"
            placeholder-class="placeholder"
          />
          <text class="toggle-password" @click.stop="showPassword = !showPassword">👁</text>
        </view>
      </view>

      <view class="form-group">
        <view class="input-wrapper">
          <text class="input-icon">🔒</text>
          <input
            v-model="confirmPassword"
            class="input-field"
            :password="!showConfirmPassword"
            placeholder="请再次输入密码"
            placeholder-class="placeholder"
          />
          <text class="toggle-password" @click.stop="showConfirmPassword = !showConfirmPassword">👁</text>
        </view>
      </view>

      <view class="form-group">
        <view class="input-wrapper">
          <text class="input-icon">😊</text>
          <input
            v-model="nickname"
            class="input-field"
            type="text"
            placeholder="2-10位昵称（可选）"
            placeholder-class="placeholder"
          />
        </view>
      </view>

      <button class="register-btn" @click="handleRegister">注册</button>

      <view class="bottom-text">
        <text>已有账号？</text>
        <text class="link" @click="goLogin">去登录</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/modules/user/store/index'
import { validateUsername, validatePassword, validateNickname } from '@/common/utils/validator'

const userStore = useUserStore()

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const nickname = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const handleBack = () => {
  uni.navigateBack({ fail: () => uni.redirectTo({ url: '/pages/login/index' }) })
}

const goLogin = () => {
  uni.redirectTo({ url: '/pages/login/index' })
}

const handleRegister = async () => {
  const usernameErr = validateUsername(username.value)
  if (usernameErr) return uni.showToast({ title: usernameErr, icon: 'none' })

  const passwordErr = validatePassword(password.value)
  if (passwordErr) return uni.showToast({ title: passwordErr, icon: 'none' })

  if (confirmPassword.value.trim() !== password.value.trim()) {
    return uni.showToast({ title: '两次密码输入不一致', icon: 'none' })
  }

  const nicknameErr = validateNickname(nickname.value)
  if (nicknameErr) return uni.showToast({ title: nicknameErr, icon: 'none' })

  try {
    await userStore.register(username.value.trim(), password.value.trim(), nickname.value.trim() || undefined)
    uni.showToast({ title: '注册成功，请登录', icon: 'success' })
    uni.redirectTo({ url: '/pages/login/index' })
  } catch {
    // request.ts 已统一toast
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
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
  padding: 80rpx 60rpx;
}

.form-group {
  margin-bottom: 40rpx;
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

.register-btn {
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

.bottom-text {
  margin-top: 40rpx;
  font-size: 28rpx;
  color: #666;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.link {
  margin-left: 10rpx;
  color: #667eea;
}
</style>

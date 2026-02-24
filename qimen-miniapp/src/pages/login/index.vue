<!-- 文档引用：PROJECT_SPEC.md - 2.2.2节 -->
<!-- 页面2：登录页 -->
<!-- UI模板参考：template/2-login.html -->

<template>
  <view class="login-page">
    <!-- 自定义导航栏（navigationStyle: custom） -->
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">登录</text>
    </view>

    <LoginForm @submit="handleLogin" @register="goRegister" @forgot="handleForgotPassword" />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import LoginForm from '@/modules/user/components/LoginForm.vue'
import { useUserStore } from '@/modules/user/store/index'
import { validateRequired, validatePassword } from '@/common/utils/validator'

const userStore = useUserStore()
const redirectUrl = ref<string>('')

onLoad((options) => {
  redirectUrl.value = options?.redirect ? decodeURIComponent(options.redirect) : ''
})

const handleBack = () => {
  uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/index/index' }) })
}

const goRegister = () => {
  uni.navigateTo({ url: '/pages/register/index' })
}

const handleForgotPassword = () => {
  uni.showModal({
    title: '提示',
    content: '请联系管理员重置密码',
    showCancel: false
  })
}

const isTabBarPage = (url: string) => {
  const tabPages = [
    '/pages/index/index',
    '/pages/qimen-input/index',
    '/pages/history-list/index',
    '/pages/profile/index'
  ]
  return tabPages.includes(url)
}

const navigateAfterLogin = () => {
  const target = redirectUrl.value
  if (target) {
    if (isTabBarPage(target)) {
      uni.switchTab({ url: target })
    } else {
      uni.redirectTo({ url: target })
    }
    return
  }

  const pages = getCurrentPages()
  if (pages.length > 1) {
    uni.navigateBack()
  } else {
    uni.switchTab({ url: '/pages/index/index' })
  }
}

const handleLogin = async (payload: { username: string; password: string }) => {
  const usernameErr = validateRequired(payload.username, '账号')
  if (usernameErr) return uni.showToast({ title: usernameErr, icon: 'none' })

  const passwordErr = validatePassword(payload.password)
  if (passwordErr) return uni.showToast({ title: passwordErr, icon: 'none' })

  try {
    await userStore.login(payload.username.trim(), payload.password)
    navigateAfterLogin()
  } catch {
    // request.ts 已统一toast，这里不重复
  }
}
</script>

<style scoped>
.login-page {
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
</style>

<!-- 文档引用：PROJECT_SPEC.md - 2.2.9节 -->
<!-- 页面9：个人中心页 -->
<!-- UI模板参考：template/9-profile.html -->

<template>
  <view class="profile-page">
    <view class="content">
      <view v-if="!isLogin" class="not-login">
        <view class="not-login-card">
          <view class="not-login-icon">👤</view>
          <text class="not-login-text">请先登录</text>
          <button class="login-btn" @click="goLogin">立即登录</button>
        </view>
      </view>

      <view v-else>
        <UserCard :userInfo="userInfo" />

        <view class="menu-list">
          <view class="menu-item" @click="openEditNickname">
            <view class="menu-left">
              <text class="menu-icon">📝</text>
              <text class="menu-label">修改资料</text>
            </view>
            <text class="menu-arrow">›</text>
          </view>
          <view class="menu-item" @click="showFeedback">
            <view class="menu-left">
              <text class="menu-icon">💬</text>
              <text class="menu-label">意见反馈</text>
            </view>
            <text class="menu-arrow">›</text>
          </view>
          <view class="menu-item" @click="goAbout">
            <view class="menu-left">
              <text class="menu-icon">ℹ️</text>
              <text class="menu-label">关于我们</text>
            </view>
            <text class="menu-arrow">›</text>
          </view>
        </view>

        <button class="logout-btn" @click="confirmLogout">退出登录</button>
      </view>
    </view>

    <!-- 修改昵称弹窗 -->
    <view v-if="editVisible" class="overlay" @click.self="closeEditNickname">
      <view class="modal">
        <text class="modal-title">修改昵称</text>
        <input
          v-model="newNickname"
          class="modal-input"
          type="text"
          placeholder="请输入新昵称（2-10位）"
          placeholder-class="placeholder"
        />
        <view class="modal-actions">
          <view class="btn cancel" @click="closeEditNickname">取消</view>
          <view class="btn confirm" @click="saveNickname">保存</view>
        </view>
      </view>
    </view>

    <!-- 意见反馈弹窗：调用 POST /api/system/feedback -->
    <view v-if="feedbackVisible" class="overlay" @click.self="closeFeedback">
      <view class="modal">
        <text class="modal-title">意见反馈</text>
        <textarea
          v-model="feedbackContent"
          class="modal-textarea"
          placeholder="请填写您的意见或建议（不少于10个字）"
          placeholder-class="placeholder"
        />
        <view class="contact-input-wrapper">
          <text class="contact-label">联系方式（选填）：</text>
          <input
            v-model="feedbackContact"
            class="contact-input"
            type="text"
            placeholder="邮箱 / 微信 / 手机号"
            placeholder-class="placeholder"
          />
        </view>
        <view class="modal-actions">
          <view class="btn cancel" @click="closeFeedback">取消</view>
          <view class="btn confirm" @click="submitFeedback">提交</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import UserCard from '@/modules/user/components/UserCard.vue'
import { useUserStore } from '@/modules/user/store/index'
import { useSystemStore } from '@/modules/system/store/index'
import { validateNickname } from '@/common/utils/validator'

const userStore = useUserStore()
const systemStore = useSystemStore()

const isLogin = computed(() => userStore.loggedIn)
const userInfo = computed(() => userStore.currentUser)

const editVisible = ref(false)
const newNickname = ref('')

// 意见反馈弹窗状态
const feedbackVisible = ref(false)
const feedbackContent = ref('')
const feedbackContact = ref('')

const goLogin = () => {
  uni.navigateTo({
    url: `/pages/login/index?redirect=${encodeURIComponent('/pages/profile/index')}`
  })
}

const goAbout = () => {
  uni.navigateTo({ url: '/pages/about/index' })
}

const openEditNickname = () => {
  newNickname.value = userInfo.value?.nickname || ''
  editVisible.value = true
}

const closeEditNickname = () => {
  editVisible.value = false
}

const saveNickname = async () => {
  const err = validateNickname(newNickname.value)
  if (err) return uni.showToast({ title: err, icon: 'none' })
  try {
    await userStore.updateUserInfo(newNickname.value.trim())
    editVisible.value = false
  } catch {
    // request.ts 已统一toast
  }
}

// 打开意见反馈弹窗
const showFeedback = () => {
  feedbackContent.value = ''
  feedbackContact.value = ''
  feedbackVisible.value = true
}

const closeFeedback = () => {
  feedbackVisible.value = false
}

const submitFeedback = async () => {
  const content = feedbackContent.value.trim()
  if (content.length < 10) {
    return uni.showToast({ title: '反馈内容不能少于10个字', icon: 'none' })
  }
  try {
    await systemStore.submitFeedback({
      content,
      contact: feedbackContact.value.trim() || undefined
    })
    feedbackVisible.value = false
  } catch {
    // systemStore.submitFeedback 内已统一 toast 错误
  }
}

const confirmLogout = () => {
  uni.showModal({
    title: '提示',
    content: '确定退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        uni.showToast({ title: '已退出', icon: 'success' })
        userStore.logout()
      }
    }
  })
}

onShow(async () => {
  if (!isLogin.value) {
    // 未登录时只展示“请先登录”卡片，不自动跳转登录页
    return
  }
  try {
    await userStore.fetchUserInfo()
  } catch {
    // fetchUserInfo 内部会 logout
  }
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.content {
  padding: 40rpx 30rpx;
}

.menu-list {
  background: #fff;
  border-radius: 20rpx;
  overflow: hidden;
  margin-bottom: 40rpx;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30rpx;
  border-bottom: 1px solid #f0f0f0;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-left {
  display: flex;
  align-items: center;
}

.menu-icon {
  font-size: 40rpx;
  margin-right: 24rpx;
}

.menu-label {
  font-size: 30rpx;
  color: #333;
}

.menu-arrow {
  color: #999;
  font-size: 32rpx;
}

.logout-btn {
  width: 100%;
  height: 100rpx;
  background: #fff;
  color: #e74c3c;
  border: none;
  border-radius: 20rpx;
  font-size: 32rpx;
  font-weight: 500;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.not-login-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 60rpx 40rpx;
  text-align: center;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.not-login-icon {
  font-size: 80rpx;
  margin-bottom: 20rpx;
}

.not-login-text {
  display: block;
  font-size: 30rpx;
  color: #333;
  margin-bottom: 40rpx;
}

.login-btn {
  width: 100%;
  height: 88rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 44rpx;
  font-size: 30rpx;
  font-weight: bold;
}

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
  padding: 40rpx 30rpx;
}

.modal-title {
  display: block;
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
  text-align: center;
}

.modal-input {
  background: #f5f5f5;
  border-radius: 16rpx;
  padding: 24rpx;
  font-size: 30rpx;
  color: #333;
}

.placeholder {
  color: #999;
}

.modal-actions {
  margin-top: 30rpx;
  display: flex;
  gap: 20rpx;
}

.btn {
  flex: 1;
  height: 80rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30rpx;
}

.cancel {
  background: #f0f0f0;
  color: #333;
}

.confirm {
  background: #667eea;
  color: #fff;
}
</style>

<template>
  <view class="ai-chat-page">
    <!-- 自定义导航栏 -->
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">问小奇</text>
    </view>

    <!-- 对话区域 -->
    <scroll-view class="chat-content" scroll-y :scroll-with-animation="true" :scroll-into-view="lastId">
      <view
        v-for="(m, idx) in messages"
        :key="idx"
        :id="`msg-${idx}`"
        class="msg-row"
        :class="m.role === 'user' ? 'msg-row-user' : 'msg-row-ai'"
      >
        <view class="avatar" v-if="m.role === 'assistant'">奇</view>
        <view class="bubble" v-text="m.content" />
        <view class="avatar user-avatar" v-if="m.role === 'user'">我</view>
      </view>

      <view v-if="loading" class="msg-row msg-row-ai loading-row">
        <view class="avatar avatar-small">奇</view>
        <view class="bubble bubble-loading">
          <view class="loading-line">
            <text>正在思考</text>
            <text class="dot dot1">·</text>
            <text class="dot dot2">·</text>
            <text class="dot dot3">·</text>
          </view>
          <text v-if="loadingHint" class="loading-hint">{{ loadingHint }}</text>
        </view>
      </view>
    </scroll-view>

    <!-- 底部输入栏 -->
    <view class="input-bar">
      <view class="len-btn" @click="chooseLen">
        <text class="len-text">长度：{{ lenLabel }}</text>
      </view>
      <input
        v-model="input"
        class="input"
        type="text"
        confirm-type="send"
        placeholder="想问什么都可以，直接输入就行"
        placeholder-class="placeholder"
        @confirm="handleSend"
      />
      <button class="send-btn" :disabled="!input.trim() || loading" @click="handleSend">发送</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad, onUnload } from '@dcloudio/uni-app'
import { aiChat, type AIChatMessage } from '@/modules/ai/api/index'

const STORAGE_KEY = 'AI_CHAT_HISTORY'

const defaultWelcome: AIChatMessage[] = [
  {
    role: 'assistant',
    content:
      '你好，我是小奇，可以跟你聊天、解答日常问题，也可以聊奇门遁甲、占卜和传统文化。有想问的就直接打字发给我吧。'
  }
]

const messages = ref<AIChatMessage[]>([...defaultWelcome])

const input = ref('')
const loading = ref(false)
const loadingSeconds = ref(0)
const loadingHint = computed(() => {
  const s = loadingSeconds.value
  if (s >= 20) return '加载中，马上就出结果了…'
  if (s >= 10) return '服务有点繁忙，请稍等一下…'
  return ''
})

let loadingTimer: ReturnType<typeof setInterval> | null = null

const startLoadingTimer = () => {
  stopLoadingTimer()
  loadingSeconds.value = 0
  loadingTimer = setInterval(() => {
    loadingSeconds.value += 1
  }, 1000)
}

const stopLoadingTimer = () => {
  if (loadingTimer) {
    clearInterval(loadingTimer)
    loadingTimer = null
  }
  loadingSeconds.value = 0
}

type LenOption = { label: string; value: number }
const lenOptions: LenOption[] = [
  { label: '简短', value: 128 },
  { label: '正常', value: 256 },
  { label: '深度', value: 512 }
]

const selectedLen = ref<number>(256)
const lenLabel = computed(() => lenOptions.find(o => o.value === selectedLen.value)?.label || '正常')

const lastId = computed(() => {
  const len = messages.value.length
  return len > 0 ? `msg-${len - 1}` : ''
})

const handleBack = () => {
  uni.navigateBack({ fail: () => uni.navigateTo({ url: '/pages/knowledge/index' }) })
}

const loadHistory = () => {
  try {
    const raw = uni.getStorageSync(STORAGE_KEY)
    if (!raw) return
    const parsed = JSON.parse(raw)
    // 简单做一个 2 小时的有效期，避免历史无限积累
    if (!parsed.updatedAt || Date.now() - parsed.updatedAt > 2 * 60 * 60 * 1000) {
      return
    }
    if (Array.isArray(parsed.messages) && parsed.messages.length) {
      messages.value = parsed.messages
    }
  } catch {
    // ignore parse error
  }
}

const saveHistory = () => {
  try {
    uni.setStorageSync(
      STORAGE_KEY,
      JSON.stringify({
        messages: messages.value,
        updatedAt: Date.now()
      })
    )
  } catch {
    // ignore
  }
}

onLoad(() => {
  loadHistory()
})

onUnload(() => {
  saveHistory()
  stopLoadingTimer()
})

const chooseLen = () => {
  uni.showActionSheet({
    itemList: lenOptions.map(o => o.label),
    success: res => {
      const idx = res.tapIndex
      if (idx >= 0 && idx < lenOptions.length) {
        selectedLen.value = lenOptions[idx].value
      }
    }
  })
}

const handleSend = async () => {
  const q = input.value.trim()
  if (!q || loading.value) return

  // 把当前问题先渲染出来
  messages.value.push({ role: 'user', content: q })
  input.value = ''
  loading.value = true
  startLoadingTimer()

  try {
    const history = messages.value.map(m => ({ role: m.role, content: m.content }))
    const res = await aiChat({ question: q, history, max_tokens: selectedLen.value })
    // 后端已经返回更新后的 history，这里直接覆盖
    messages.value = res.history || history
    saveHistory()
  } catch {
    uni.showToast({ title: '小奇忙不过来，请稍后再试', icon: 'none' })
  } finally {
    loading.value = false
    stopLoadingTimer()
  }
}
</script>

<style scoped>
.ai-chat-page {
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

.chat-content {
  flex: 1;
  padding: 30rpx 24rpx 20rpx;
  box-sizing: border-box;
}

.msg-row {
  display: flex;
  margin-bottom: 20rpx;
}

.msg-row-ai {
  justify-content: flex-start;
}

.msg-row-user {
  justify-content: flex-end;
}

.avatar {
  width: 64rpx;
  height: 64rpx;
  border-radius: 32rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 26rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16rpx;
}

.avatar-small {
  width: 52rpx;
  height: 52rpx;
  font-size: 24rpx;
}

.user-avatar {
  margin-left: 16rpx;
  margin-right: 0;
  background: #f0f0f0;
  color: #666;
}

.bubble {
  max-width: 70%;
  padding: 18rpx 24rpx;
  border-radius: 24rpx;
  font-size: 28rpx;
  line-height: 1.6;
  color: #333;
  background: #ffffff;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.msg-row-user .bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.bubble-loading {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 10rpx 16rpx;
  font-size: 24rpx;
  color: #666;
  background: #f0f0f0;
}

.loading-line {
  display: flex;
  align-items: center;
  gap: 4rpx;
}

.loading-hint {
  margin-top: 8rpx;
  font-size: 22rpx;
  color: #888;
}

.loading-row {
  margin-top: 8rpx;
}

.dot {
  font-size: 32rpx;
  opacity: 0.3;
  animation: blink 1.2s infinite ease-in-out;
}

.dot2 {
  animation-delay: 0.2s;
}

.dot3 {
  animation-delay: 0.4s;
}

@keyframes blink {
  0%,
  80%,
  100% {
    opacity: 0.2;
    transform: translateY(0);
  }
  40% {
    opacity: 0.9;
    transform: translateY(-4rpx);
  }
}

.input-bar {
  padding: 16rpx 24rpx 24rpx;
  background: #fff;
  display: flex;
  align-items: center;
  box-shadow: 0 -2rpx 6rpx rgba(0, 0, 0, 0.03);
}

.len-btn {
  height: 72rpx;
  padding: 0 18rpx;
  border-radius: 36rpx;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  margin-right: 14rpx;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.len-text {
  font-size: 24rpx;
  color: #666;
  white-space: nowrap;
}

.input {
  flex: 1;
  height: 72rpx;
  border-radius: 36rpx;
  padding: 0 24rpx;
  background: #f5f5f5;
  font-size: 28rpx;
  margin-right: 14rpx;
}

.placeholder {
  color: #999;
}

.send-btn {
  width: 140rpx;
  height: 72rpx;
  border-radius: 36rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  font-size: 28rpx;
}

.send-btn:disabled {
  opacity: 0.5;
}
</style>


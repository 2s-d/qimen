<!-- 文档引用：PROJECT_SPEC.md - 2.2.6节 -->
<!-- 页面6：解读结果页 -->
<!-- UI模板参考：template/6-result.html -->

<template>
  <view class="qimen-result-page">
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">运势解读</text>
    </view>

    <scroll-view class="content" scroll-y>
      <view class="overall-card" v-if="fortune">
        <view class="overall-title">总体运势</view>
        <view class="overall-rating">{{ overallStars }} {{ fortune.overall_score }}分</view>
        <view class="overall-level">吉凶：{{ fortune.overall_fortune }}</view>
      </view>

      <FortuneCard
        v-if="fortune"
        title="事业运"
        icon="💼"
        :stars="stars(fortune.fortunes?.career?.score)"
        :desc="fortune.fortunes?.career?.text || ''"
      />
      <FortuneCard
        v-if="fortune"
        title="财运"
        icon="💰"
        :stars="stars(fortune.fortunes?.wealth?.score)"
        :desc="fortune.fortunes?.wealth?.text || ''"
      />
      <FortuneCard
        v-if="fortune"
        title="感情运"
        icon="💕"
        :stars="stars(fortune.fortunes?.love?.score)"
        :desc="fortune.fortunes?.love?.text || ''"
      />
      <FortuneCard
        v-if="fortune"
        title="健康运"
        icon="🏥"
        :stars="stars(fortune.fortunes?.health?.score)"
        :desc="fortune.fortunes?.health?.text || ''"
      />

      <view class="notice-card" v-if="fortune">
        <view class="notice-title">⚠️ 注意事项</view>
        <view class="notice-list">
          <view v-for="(n, idx) in fortune.notices || []" :key="idx" class="notice-item">{{ n }}</view>
        </view>
      </view>

      <view class="action-buttons">
        <button class="btn btn-primary" @click="goHome">返回首页</button>
        <button class="btn btn-secondary" @click="goPlate">查看盘面</button>
      </view>

      <view v-if="!fortune" class="empty">
        <text class="empty-text">暂无解读数据</text>
        <button class="btn btn-primary" @click="goHome">返回首页</button>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import FortuneCard from '@/modules/qimen/components/FortuneCard.vue'
import { useQimenStore } from '@/modules/qimen/store/index'
import { formatStar } from '@/common/utils/format'

const qimenStore = useQimenStore()
const mode = ref<'fortune' | 'plate'>('plate')

onLoad((options) => {
  const m = options?.mode
  mode.value = m === 'fortune' ? 'fortune' : 'plate'
})

const fortune = computed(() => {
  if (mode.value === 'fortune') return qimenStore.dailyFortune
  return qimenStore.currentPlate?.fortune_data || null
})

const overallStars = computed(() => formatStar(fortune.value?.overall_score || 0))

const stars = (score?: number) => formatStar(score || 0)

const handleBack = () => {
  uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/index/index' }) })
}

const goHome = () => {
  uni.switchTab({ url: '/pages/index/index' })
}

const goPlate = () => {
  uni.navigateTo({ url: '/pages/qimen-plate/index' })
}
</script>

<style scoped>
.qimen-result-page {
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

.content {
  flex: 1;
  padding: 30rpx;
  height: 0;
}

.overall-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 24rpx;
  text-align: center;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
}

.overall-title {
  font-size: 30rpx;
  color: #666;
  margin-bottom: 16rpx;
}

.overall-rating {
  color: #ffd700;
  font-size: 34rpx;
  margin-bottom: 12rpx;
}

.overall-level {
  color: #27ae60;
  font-size: 28rpx;
}

.notice-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-top: 10rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
}

.notice-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 16rpx;
}

.notice-item {
  font-size: 26rpx;
  color: #666;
  line-height: 1.8;
  padding-left: 20rpx;
  position: relative;
}

.notice-item::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #667eea;
}

.action-buttons {
  display: flex;
  gap: 20rpx;
  margin-top: 10rpx;
}

.btn {
  flex: 1;
  height: 88rpx;
  border-radius: 44rpx;
  font-size: 30rpx;
  font-weight: 500;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.btn-secondary {
  background: #fff;
  color: #667eea;
  border-width: 4rpx;
  border-style: solid;
  border-color: #667eea;
}

.empty {
  background: #fff;
  border-radius: 20rpx;
  padding: 60rpx 40rpx;
  text-align: center;
}

.empty-text {
  display: block;
  font-size: 28rpx;
  color: #999;
  margin-bottom: 30rpx;
}
</style>

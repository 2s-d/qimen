<!-- 文档引用：PROJECT_SPEC.md - 2.2.5节 -->
<!-- 页面5：盘面展示页 -->
<!-- UI模板参考：template/5-plate-display.html -->

<template>
  <view class="qimen-plate-page">
    <view class="navbar">
      <view class="back-btn" @click="handleBack">‹ 返回</view>
      <text class="nav-title">奇门盘面</text>
    </view>

    <scroll-view class="content" scroll-y>
      <view class="info-bar" v-if="plate">
        📅 {{ plate.datetime }} {{ plate.gender }}<br />
        值符：{{ plate.chief_star }} &nbsp; 值使：{{ plate.chief_door }}
      </view>

      <view class="plate-container" v-if="plate">
        <PlateGrid :palaces="palaceList" @select="openPalace" />
      </view>

      <view class="action-buttons" v-if="plate">
        <button class="btn btn-primary" @click="goResult">查看解读</button>
        <button class="btn btn-secondary" @click="saveRecord">保存记录</button>
      </view>

      <view v-if="!plate" class="empty">
        <text class="empty-text">暂无盘面数据，请先起盘</text>
        <button class="btn btn-primary" @click="goInput">去起盘</button>
      </view>
    </scroll-view>

    <PalaceDetail :visible="palaceVisible" :palace="selectedPalace" @close="closePalace" />
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useQimenStore } from '@/modules/qimen/store/index'
import PlateGrid from '@/modules/qimen/components/PlateGrid.vue'
import PalaceDetail from '@/modules/qimen/components/PalaceDetail.vue'

const qimenStore = useQimenStore()

const plate = computed(() => qimenStore.currentPlate)
const palaceVisible = ref(false)
const selectedPalace = ref<any | null>(null)

const palaceList = computed(() => {
  const p = plate.value
  if (!p?.palaces) return []
  return (p.palaces as any[]).map((x) => ({
    ...x,
    highlight: x.heaven_star === p.chief_star || x.human_door === p.chief_door
  }))
})

const handleBack = () => {
  uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/qimen-input/index' }) })
}

const openPalace = (p: any) => {
  selectedPalace.value = p
  palaceVisible.value = true
}

const closePalace = () => {
  palaceVisible.value = false
  selectedPalace.value = null
}

const goResult = () => {
  uni.navigateTo({ url: '/pages/qimen-result/index?mode=plate' })
}

const goInput = () => {
  uni.switchTab({ url: '/pages/qimen-input/index' })
}

const saveRecord = async () => {
  if (!plate.value) return
  try {
    await qimenStore.saveQimenRecord({
      datetime: plate.value.datetime,
      gender: plate.value.gender,
      type: plate.value.type,
      plate_data: {
        datetime: plate.value.datetime,
        gender: plate.value.gender,
        type: plate.value.type,
        chief_star: plate.value.chief_star,
        chief_door: plate.value.chief_door,
        palaces: plate.value.palaces
      },
      fortune_data: plate.value.fortune_data,
      fortune_score: plate.value.fortune_data?.overall_score || 0
    })
  } catch {
    // request.ts 已统一toast
  }
}
</script>

<style scoped>
.qimen-plate-page {
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

.info-bar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 24rpx 30rpx;
  border-radius: 20rpx;
  margin-bottom: 24rpx;
  font-size: 26rpx;
  line-height: 1.6;
}

.plate-container {
  background: #fff;
  padding: 30rpx;
  border-radius: 20rpx;
  margin-bottom: 24rpx;
}

.action-buttons {
  display: flex;
  gap: 20rpx;
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

<!-- 文档引用：PROJECT_SPEC.md - 1286行 -->
<!-- 日期时辰选择器组件（起盘输入页使用） -->

<template>
  <view class="datetime-picker">
    <view class="form-section">
      <view class="section-title">
        <text class="section-icon">📅</text>
        <text>公历/农历切换</text>
      </view>
      <view class="radio-group">
        <view class="radio-item" @click="setCalendarType('solar')">
          <view class="radio-circle" :class="{ active: calendarType === 'solar' }" />
          <text class="radio-label">公历</text>
        </view>
        <view class="radio-item" @click="setCalendarType('lunar')">
          <view class="radio-circle" :class="{ active: calendarType === 'lunar' }" />
          <text class="radio-label">农历</text>
        </view>
      </view>
    </view>

    <view class="form-section">
      <view class="section-title">
        <text class="section-icon">📅</text>
        <text>选择日期</text>
      </view>
      <picker mode="date" :value="inner.date" start="1900-01-01" end="2100-12-31" @change="onDateChange">
        <view class="select-box">
          <text class="select-value">{{ displayDate }}</text>
          <text class="select-arrow">▼</text>
        </view>
      </picker>
    </view>

    <view class="form-section">
      <view class="section-title">
        <text class="section-icon">🕐</text>
        <text>选择时辰</text>
      </view>
      <picker mode="selector" :range="shichenOptions" :value="shichenIndex" @change="onShichenChange">
        <view class="select-box">
          <text class="select-value">{{ displayShichen }}</text>
          <text class="select-arrow">▼</text>
        </view>
      </picker>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, reactive, watch } from 'vue'

const props = defineProps<{
  modelValue: {
    calendarType: 'solar' | 'lunar'
    date: string
    shichen: string
  }
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: { calendarType: 'solar' | 'lunar'; date: string; shichen: string }): void
}>()

const inner = reactive({ ...props.modelValue })

watch(
  () => props.modelValue,
  (v) => {
    Object.assign(inner, v)
  },
  { deep: true }
)

const calendarType = computed(() => inner.calendarType)

const displayDate = computed(() => {
  return inner.date || '请选择日期'
})

const displayShichen = computed(() => {
  return inner.shichen || '请选择时辰'
})

const sync = () => {
  emit('update:modelValue', { ...inner })
}

const setCalendarType = (type: 'solar' | 'lunar') => {
  inner.calendarType = type
  sync()
}

const onDateChange = (e: any) => {
  inner.date = e.detail.value
  sync()
}

const shichenOptions = [
  '子时(23:00-01:00)',
  '丑时(01:00-03:00)',
  '寅时(03:00-05:00)',
  '卯时(05:00-07:00)',
  '辰时(07:00-09:00)',
  '巳时(09:00-11:00)',
  '午时(11:00-13:00)',
  '未时(13:00-15:00)',
  '申时(15:00-17:00)',
  '酉时(17:00-19:00)',
  '戌时(19:00-21:00)',
  '亥时(21:00-23:00)'
]

const shichenIndex = computed(() => {
  const idx = shichenOptions.findIndex(x => x === inner.shichen)
  return idx >= 0 ? idx : 0
})

const onShichenChange = (e: any) => {
  const idx = Number(e.detail.value)
  inner.shichen = shichenOptions[idx]
  sync()
}
</script>

<style scoped>
.datetime-picker {
  width: 100%;
}

.form-section {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 28rpx;
  color: #666;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
}

.section-icon {
  margin-right: 12rpx;
  font-size: 30rpx;
}

.radio-group {
  display: flex;
  gap: 40rpx;
}

.radio-item {
  display: flex;
  align-items: center;
}

.radio-circle {
  width: 32rpx;
  height: 32rpx;
  border-radius: 16rpx;
  border-width: 4rpx;
  border-style: solid;
  border-color: #ddd;
  margin-right: 12rpx;
  position: relative;
}

.radio-circle.active {
  border-color: #667eea;
}

.radio-circle.active::after {
  content: '';
  position: absolute;
  width: 18rpx;
  height: 18rpx;
  border-radius: 9rpx;
  background: #667eea;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.radio-label {
  font-size: 28rpx;
  color: #333;
}

.select-box {
  background: #f8f8f8;
  border-radius: 16rpx;
  padding: 24rpx 30rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.select-value {
  font-size: 28rpx;
  color: #333;
}

.select-arrow {
  color: #999;
  font-size: 26rpx;
}
</style>


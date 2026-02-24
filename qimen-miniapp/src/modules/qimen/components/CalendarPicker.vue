<!-- 文档引用：PROJECT_SPEC.md - 1422行 -->
<!-- 万年历日历选择器组件 -->

<template>
  <view class="calendar-wrapper">
    <view class="month-selector">
      <text class="month-arrow" @click="changeMonth(-1)">‹</text>
      <text class="month-text">{{ year }}年{{ month }}月</text>
      <text class="month-arrow" @click="changeMonth(1)">›</text>
    </view>
    <view class="calendar-container">
      <view class="weekdays">
        <text v-for="d in weekdays" :key="d" class="weekday">{{ d }}</text>
      </view>
      <view class="days">
        <view v-for="(cell, idx) in cells" :key="idx" :class="['day', cell.type, dayClass(cell)]" @click="handleSelect(cell)">
          <text v-if="cell.type === 'normal'">{{ cell.day }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  year: number
  month: number
  days: { day: number; isToday?: boolean; isSelected?: boolean }[]
}>()

const emit = defineEmits<{
  (e: 'changeMonth', payload: { year: number; month: number }): void
  (e: 'selectDay', payload: { day: number }): void
}>()

const weekdays = ['日', '一', '二', '三', '四', '五', '六']

const cells = computed(() => {
  const first = new Date(props.year, props.month - 1, 1)
  const startWeek = first.getDay()
  const result: { type: 'empty' | 'normal'; day?: number; isToday?: boolean; isSelected?: boolean }[] = []
  for (let i = 0; i < startWeek; i++) {
    result.push({ type: 'empty' })
  }
  props.days.forEach(d => {
    result.push({ type: 'normal', ...d })
  })
  return result
})

const changeMonth = (delta: number) => {
  let y = props.year
  let m = props.month + delta
  if (m < 1) {
    m = 12
    y--
  } else if (m > 12) {
    m = 1
    y++
  }
  emit('changeMonth', { year: y, month: m })
}

const handleSelect = (cell: any) => {
  if (cell.type !== 'normal' || !cell.day) return
  emit('selectDay', { day: cell.day })
}

const dayClass = (cell: any) => {
  if (cell.type !== 'normal') return ''
  if (cell.isSelected) return 'selected'
  if (cell.isToday) return 'today'
  return ''
}
</script>

<style scoped>
.calendar-wrapper {
  width: 100%;
}

.month-selector {
  background: #fff;
  border-radius: 20rpx;
  padding: 20rpx 30rpx;
  margin-bottom: 24rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.month-arrow {
  font-size: 36rpx;
  color: #667eea;
}

.month-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.calendar-container {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10rpx;
  margin-bottom: 10rpx;
}

.weekday {
  text-align: center;
  font-size: 24rpx;
  color: #666;
}

.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10rpx;
}

.day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26rpx;
  border-radius: 10rpx;
}

.day.normal {
  color: #333;
}

.day.empty {
  background: transparent;
}

.day.today {
  background: #667eea;
  color: #fff;
  font-weight: bold;
}

.day.selected {
  background: #764ba2;
  color: #fff;
}
</style>


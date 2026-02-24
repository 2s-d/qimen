<!-- 文档引用：PROJECT_SPEC.md - 1418行 -->
<!-- 九宫格盘面组件 -->

<template>
  <view class="plate-grid">
    <view
      v-for="palace in palaces"
      :key="palace.position"
      class="palace"
      :class="{ highlight: palace.highlight }"
      @click="handleClick(palace)"
    >
      <text class="palace-position">{{ palace.position }}</text>
      <text class="palace-star">{{ palace.heaven_star }}</text>
      <text class="palace-door">{{ palace.human_door }}</text>
      <text class="palace-god">{{ palace.god }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
interface PalaceData {
  position: string
  heaven_star: string
  earth_palace?: string
  human_door: string
  god: string
  highlight?: boolean
  [key: string]: any
}

const props = defineProps<{
  palaces: PalaceData[]
}>()

const emit = defineEmits<{
  (e: 'select', palace: PalaceData): void
}>()

const handleClick = (palace: PalaceData) => {
  emit('select', palace)
}
</script>

<style scoped>
.plate-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16rpx;
}

.palace {
  background: #f8f8f8;
  border: 2rpx solid #e0e0e0;
  border-radius: 16rpx;
  padding: 16rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 22rpx;
  line-height: 1.4;
}

.palace.highlight {
  border-color: #ffd700;
  background: #fffef0;
  box-shadow: 0 0 16rpx rgba(255, 215, 0, 0.3);
}

.palace-position {
  font-weight: bold;
  color: #333;
  margin-bottom: 4rpx;
}

.palace-star {
  color: #667eea;
}

.palace-door {
  color: #e74c3c;
}

.palace-god {
  color: #27ae60;
}
</style>


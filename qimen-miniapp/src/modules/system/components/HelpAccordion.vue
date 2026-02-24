<!-- 文档引用：PROJECT_SPEC.md - 1301行 -->
<!-- 帮助折叠面板 - 接收帮助问题列表，点击展开/收起 -->

<template>
  <view class="help-accordion">
    <view
      v-for="(item, index) in questions"
      :key="index"
      class="help-item"
      @click="toggle(index)"
    >
      <view class="help-question">
        <text class="help-icon">❓</text>
        <text class="help-text">{{ item.question }}</text>
        <text class="help-arrow">{{ expandedIndex === index ? '▲' : '▼' }}</text>
      </view>
      <view v-show="expandedIndex === index" class="help-answer">
        <text class="answer-text">{{ item.answer }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
// 文档引用：PROJECT_SPEC.md - 1301行
// 手风琴效果：展开一个自动收起其他

interface HelpQuestion {
  question: string
  answer: string
}

defineProps<{
  questions: HelpQuestion[]
}>()

import { ref } from 'vue'

const expandedIndex = ref(-1)

const toggle = (index: number) => {
  expandedIndex.value = expandedIndex.value === index ? -1 : index
}
</script>

<style scoped>
.help-accordion {
  width: 100%;
}

.help-item {
  border-bottom: 1px solid #f0f0f0;
}

.help-item:last-child {
  border-bottom: none;
}

.help-question {
  display: flex;
  align-items: center;
  padding: 20rpx 0;
  cursor: pointer;
}

.help-icon {
  margin-right: 16rpx;
  font-size: 28rpx;
}

.help-text {
  flex: 1;
  font-size: 28rpx;
  color: #333;
}

.help-arrow {
  font-size: 24rpx;
  color: #999;
}

.help-answer {
  padding: 0 0 24rpx 44rpx;
}

.answer-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.8;
  white-space: pre-wrap;
}
</style>

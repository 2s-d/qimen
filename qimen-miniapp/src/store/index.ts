// 文档引用：PROJECT_SPEC.md - 1342行
// 汇总各模块store

import { createPinia } from 'pinia'

const pinia = createPinia()

export { useSystemStore } from '@/modules/system/store/index'
export { useQimenStore } from '@/modules/qimen/store/index'
export { useUserStore } from '@/modules/user/store/index'

export default pinia

// 文档引用：PROJECT_SPEC.md - 1319行
// 格式化工具

/**
 * 格式化日期
 * @param date - 日期对象或日期字符串
 * @param fmt - 格式字符串，如 'YYYY-MM-DD'
 * @returns 格式化后的日期字符串
 */
export const formatDate = (date: Date | string, fmt: string = 'YYYY-MM-DD'): string => {
  if (!date) return ''
  const d = new Date(date)
  const o: Record<string, number> = {
    'M+': d.getMonth() + 1, // 月份
    'D+': d.getDate(), // 日
    'h+': d.getHours() % 12 === 0 ? 12 : d.getHours() % 12, // 小时
    'H+': d.getHours(), // 小时
    'm+': d.getMinutes(), // 分
    's+': d.getSeconds(), // 秒
    'q+': Math.floor((d.getMonth() + 3) / 3), // 季度
    'S': d.getMilliseconds() // 毫秒
  }
  if (/(Y+)/.test(fmt)) {
    fmt = fmt.replace(RegExp.$1, (d.getFullYear() + '').substr(4 - RegExp.$1.length))
  }
  for (const k in o) {
    if (new RegExp('(' + k + ')').test(fmt)) {
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k] + '') : (('00' + o[k]).substr(('' + o[k]).length)))
    }
  }
  return fmt
}

/**
 * 格式化日期时间
 * @param date - 日期对象或日期字符串
 * @param fmt - 格式字符串，如 'YYYY-MM-DD HH:mm:ss'
 * @returns 格式化后的日期时间字符串
 */
export const formatDateTime = (date: Date | string, fmt: string = 'YYYY-MM-DD HH:mm:ss'): string => {
  return formatDate(date, fmt)
}

/**
 * 格式化星级评分
 * @param score - 评分，例如 4.0
 * @returns 星星图标字符串，例如 "★★★★☆"
 */
export const formatStar = (score: number): string => {
  if (typeof score !== 'number' || score < 0 || score > 5) {
    return '☆☆☆☆☆'
  }
  const fullStars = Math.floor(score)
  const halfStar = score % 1 >= 0.5 ? '★' : '' // uni-app 不支持半星图标，用全星代替
  const emptyStars = 5 - fullStars - (halfStar ? 1 : 0)
  return '★'.repeat(fullStars) + halfStar + '☆'.repeat(emptyStars)
}

/**
 * 格式化数字为千分位
 * @param num - 数字
 * @returns 格式化后的字符串
 */
export const formatNumber = (num: number): string => {
  if (typeof num !== 'number') return String(num)
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// 文档引用：PROJECT_SPEC.md - 1317行
// 表单验证工具

const USERNAME_REGEX = /^[a-zA-Z0-9_]{3,20}$/

export const validateRequired = (value: string, fieldName: string): string | null => {
  if (!value || !value.trim()) return `${fieldName}不能为空`
  return null
}

export const validateUsername = (username: string): string | null => {
  const required = validateRequired(username, '账号')
  if (required) return required
  if (!USERNAME_REGEX.test(username.trim())) return '用户名需为3-20位字母/数字/下划线'
  return null
}

export const validatePassword = (password: string): string | null => {
  const required = validateRequired(password, '密码')
  if (required) return required
  const len = password.trim().length
  if (len < 6) return '密码长度不能少于6位'
  if (len > 20) return '密码长度不能超过20位'
  return null
}

export const validateNickname = (nickname?: string): string | null => {
  if (!nickname) return null
  const trimmed = nickname.trim()
  if (!trimmed) return null
  if (trimmed.length < 2) return '昵称长度不能少于2位'
  if (trimmed.length > 10) return '昵称长度不能超过10位'
  return null
}


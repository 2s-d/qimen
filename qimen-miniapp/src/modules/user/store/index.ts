// 文档引用：PROJECT_SPEC.md - 1274行
// 用户模块状态管理

import { defineStore } from 'pinia'
import { registerUser as apiRegisterUser, loginUser as apiLoginUser, getUserInfo as apiGetUserInfo, updateUserInfo as apiUpdateUserInfo } from '../api/index'
import { setToken, getToken, removeToken, setUserInfo, getUserInfo, removeUserInfo } from '@/common/utils/storage'
import { redirectToLogin } from '../utils/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: getToken(),
    userInfo: getUserInfo(),
    isLogin: !!getToken()
  }),
  getters: {
    loggedIn: (state) => !!state.token,
    currentUser: (state) => state.userInfo
  },
  actions: {
    async register(username: string, password: string, nickname?: string) {
      try {
        const res = await apiRegisterUser({ username, password, nickname })
        return res
      } catch (error) {
        console.error('注册失败:', error)
        throw error
      }
    },
    async login(username: string, password: string) {
      try {
        const res = await apiLoginUser({ username, password })
        // 文档引用：PROJECT_SPEC.md - 2451行，响应格式：{token: "...", user: {...}}
        this.token = res.token
        this.isLogin = true
        setToken(res.token)
        // 存储用户信息
        if (res.user) {
          this.userInfo = res.user
          setUserInfo(res.user)
        } else {
          await this.fetchUserInfo() // 如果没有返回user，则获取用户信息
        }
        uni.showToast({ title: '登录成功', icon: 'success' })
        return res
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    },
    async fetchUserInfo() {
      if (!this.token) {
        this.userInfo = null
        this.isLogin = false
        removeUserInfo()
        return null
      }
      try {
        const res = await apiGetUserInfo()
        this.userInfo = res
        setUserInfo(res)
        return res
      } catch (error) {
        console.error('获取用户信息失败:', error)
        // Token可能过期或无效，执行登出
        this.logout()
        throw error
      }
    },
    async updateUserInfo(nickname: string) {
      try {
        const res = await apiUpdateUserInfo({ nickname })
        this.userInfo = { ...this.userInfo, nickname: res.nickname }
        setUserInfo(this.userInfo)
        uni.showToast({ title: '更新成功', icon: 'success' })
        return res
      } catch (error) {
        console.error('更新用户信息失败:', error)
        throw error
      }
    },
    logout() {
      this.token = null
      this.userInfo = null
      this.isLogin = false
      removeToken()
      removeUserInfo()
      redirectToLogin() // 登出后跳转到登录页
    }
  }
})

import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    userId: null
  }),
  actions: {
    async checkAuth() {
      try {
        const response = await fetch('/api/v1/auth/status', {
          credentials: 'include'
        })
        const data = await response.json()
        this.isLoggedIn = data.logged_in
        this.userId = data.user_id || null
      } catch {
        this.isLoggedIn = false
        this.userId = null
      }
    },
    setLoggedIn(userId) {
      this.isLoggedIn = true
      this.userId = userId
    },
    setLoggedOut() {
      this.isLoggedIn = false
      this.userId = null
    }
  }
})
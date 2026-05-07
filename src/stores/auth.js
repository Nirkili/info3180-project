<<<<<<< HEAD
// References:
//  https://pinia.vuejs.org/core-concepts/
//  https://jasonwatmore.com/post/2022/07/25/vue-3-pinia-user-registration-and-login-example-tutorial

import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    userId: null,
    firstName: null,
    lastName: null
  }),



  // Function to check if the user is authenticates
  actions: {
    async checkAuth() {
      try {
        // Call the auth_status route from flask
        // This will return True and the current users ID or False
        const response = await fetch('/api/v1/auth/status', {
          credentials: 'include'
        })
        const data = await response.json()
        this.isLoggedIn = data.logged_in
        
        // Set userID to null if there is no current user
        this.userId = data.user_id || null
      } 
      
      catch {
        this.isLoggedIn = false
        this.userId = null
      }
    },

    // This function stores the current user's information on login
    setLoggedIn(userId, firstName, lastName) {
      this.isLoggedIn = true
      this.userId = userId
      this.firstName=firstName
      this.lastName = lastName

    },

    // This function removes the current user's information on logout
    setLoggedOut() {
      this.isLoggedIn = false
      this.userId = null
      this.firstName=null
      this.lastName = null
    }
  }
=======
// References:
//  https://pinia.vuejs.org/core-concepts/
//  https://jasonwatmore.com/post/2022/07/25/vue-3-pinia-user-registration-and-login-example-tutorial

import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    userId: null,
    firstName: null,
    lastName: null
  }),



  // Function to check if the user is authenticates
  actions: {
    async checkAuth() {
      try {
        // Call the auth_status route from flask
        // This will return True and the current users ID or False
        const response = await fetch('/api/v1/auth/status', {
          credentials: 'include'
        })
        const data = await response.json()
        this.isLoggedIn = data.logged_in
        
        // Set userID to null if there is no current user
        this.userId = data.user_id || null
      } 
      
      catch {
        this.isLoggedIn = false
        this.userId = null
      }
    },

    // This function stores the current user's information on login
    setLoggedIn(userId, firstName, lastName) {
      this.isLoggedIn = true
      this.userId = userId
      this.firstName=firstName
      this.lastName = lastName

    },

    // This function removes the current user's information on logout
    setLoggedOut() {
      this.isLoggedIn = false
      this.userId = null
      this.firstName=null
      this.lastName = null
    }
  }
>>>>>>> origin/Jaden
})
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },

    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },

     {
      path: '/community_guidelines',
      name: 'community_guidelines',
      component: () => import('../views/GuidelinesView.vue')
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },

    {
      path: '/register_user',
      name: 'register_user',
      component: () => import('../views/Register.vue')
    },

    {
      path: '/register_interest',
      name: 'register_interest',
      component: () => import('../views/Register_Interest.vue')
    },

    {
      path: '/my_profile',
      name: 'my_profile',
      component: () => import('../views/Profile.vue')
    },

    {
      path: '/search_profiles',
      name: 'search_profiles',
      component: () => import('../views/SearchProfiles.vue')
    }

  ]
})

export default router

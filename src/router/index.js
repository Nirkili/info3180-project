import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
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
      component: () => import('../views/Login.vue'),
      meta: {noBackground: true}
    },  

    {
      path: '/register_user',
      name: 'register_user',
      component: () => import('../views/Register.vue'),
      meta:{noBackground: true}
    },

    {
      path: '/register_interest',
      name: 'register_interest',
      component: () => import('../views/Register_Interest.vue'),
      meta: {noBackground: true}
    },
    

    {
      path: '/home',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true }
    },

    {
      path: '/my_profile',
      name: 'my_profile',
      component: () => import('../views/Profile.vue'),
      meta: { requiresAuth: true }
    },

    {
      path: '/search_profiles',
      name: 'search_profiles',
      component: () => import('../views/SearchProfiles.vue'),
      meta: { requiresAuth: true }
    },

    {
      path: '/matches',
      name: 'matches',
      component: () => import('../views/MatchesView.vue'),
      meta: { requiresAuth: true }
    },

    {
      path: '/bookmarks',
      name: 'bookmarks',
      component: () => import('../views/BookmarksView.vue'),
      meta: { requiresAuth: true }
    },

    {
      path: '/messages',
      name: 'messages',
      component: () => import('../views/MessagesView.vue'),
      meta: { requiresAuth: true }
    }

  ]
})


router.beforeEach(async(to, form, next) =>{

  // Check logged in status
  let isLoggedIn = false;

  try{
    const response = await fetch('/api/v1/auth/status', {
        credentials: 'include'
      })
      const data = await response.json()
      isLoggedIn = data.logged_in;
  }

  catch(error){
    isLoggedIn = false;
  }

  const authRoutes = ['login', 'register_user']

  if(to.meta.requiresAuth && !isLoggedIn){
    next('/login')
  }

  else if(authRoutes.includes(to.name) && isLoggedIn){
    next('/home')
  }

  else if(to.path === '/'){
    next(isLoggedIn ? 'home': '/login')
  }

  else{
    next()
  }
})

/*router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const response = await fetch('/api/v1/auth/status', {
        credentials: 'include'
      })
      const data = await response.json()

      if (data.logged_in) {
        next()
      } else {
        next('/login')
      }
    } catch (error) {
      next('/login')
    }
  } else {
    next()
  }

})*/

export default router

<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import AppSidebar from "@/components/AppSidebar.vue";
import { ref } from 'vue';

const route = useRoute()
const router = useRouter()
const isRouterReady = ref(false)
router.isReady().then(() => isRouterReady.value = true)

const hideSidebarOn = ['login', 'register_user', 'register_interest', 'about', 'community_guidelines']
</script>

<template>
  <div v-if="isRouterReady">
    <AppHeader />

  <div class="layout">
    <AppSidebar v-if="!hideSidebarOn.includes(route.name)"/>

    <main :class="['main-content', { 'noBackground': $route.meta.noBackground }]">
    <RouterView />
  </main>

  </div>
  </div>
</template>

<style>
body{
  background-image: radial-gradient(circle at bottom right, #E95DA1 1%,#4a154b 40%, #1a061c 65%, #0d0d0d 100%);
  margin: 0;
  font-family: 'Inter', sans-serif;
}

.layout{
  margin-top: 100px;
  display: flex;
  padding: 20px;
  gap: 20px;
  height: calc(100vh - 100px);
  overflow: hidden;
}

.main-content {
  flex: 1;
  background-color: none;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  height: 100%;
  overflow-y: auto;
  box-shadow: 0 0 10px rgba(95, 10, 164, 0.1);
}

/* Chrome, Edge, Safari */
.main-content::-webkit-scrollbar {
  display: none;
}

/* Firefox */
.main-content {
  scrollbar-width: none;
}

.main-content {
  -ms-overflow-style: none; 
}

.nav-bar::-webkit-scrollbar {
  display: none;
}

.noBackground{
  background-color: transparent !important;
}
</style>
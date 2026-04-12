<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import AppSidebar from "@/components/AppSidebar.vue";

const route = useRoute()

const hideSidebarOn = ['login', 'register_user', 'about', 'community_guidelines']
</script>

<template>
  <AppHeader />

  <div class="layout">
    <AppSidebar v-if="!hideSidebarOn.includes(route.name)"/>

    <main class="main-content">
    <RouterView />
  </main>

  </div>
</template>

<style>
body{
  /*background-color: rgb(242, 239, 243);*/
  background-image: linear-gradient(to bottom right, rgb(0, 0, 0), rgb(85, 13, 103));
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
  background-color: white;
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

</style>
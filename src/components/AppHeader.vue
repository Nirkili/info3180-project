<script setup>
import {ref, onMounted} from "vue";
import { useRouter, RouterLink } from "vue-router";
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();
let csrf_token = ref("");
let successMessage = ref("");
let errorMessages = ref([])

  onMounted(() => {
    getCsrfToken();
    authStore.checkAuth();
  })

  function getCsrfToken() {
    return fetch('/api/v1/csrf-token')
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        csrf_token.value = data.csrf_token
      })
      .catch((error) => {
        console.log(error)
      })
}


function logout(){
  fetch('/api/v1/auth/logout', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })

  .then(function(response){
    if(!response.ok){
      throw new Error(`Server error: ${response.status}`)
    }
    return response.json()
  })

  .then(function(data){
    console.log(data)
    authStore.setLoggedOut()
    router.push('/login')
  })

  .catch(function(error){
  errorMessages.value = [error.message]
})

  }

</script>

<template>
  <header>
    <div class="header-wrapper">
    <nav class="navbar navbar-expand-lg navbar-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">DriftDater</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item mx-3" >
              <RouterLink to="/about" class="nav-link active">About Us</RouterLink>
            </li>
            <li class="nav-item mx-3">
              <RouterLink class="nav-link" to="/community_guidelines">Community Guidelines</RouterLink>
            </li>
            <li class="nav-item mx-3" v-if="authStore.isLoggedIn">
              <RouterLink class="nav-link" to="/my_profile">My Profile</RouterLink>
            </li>
             <li class="nav-item mx-3" v-if="authStore.isLoggedIn">
              <RouterLink class="nav-link" to="/search_profiles">Search Profiles</RouterLink>
            </li>
          </ul>

          <ul class="navbar-nav ms-auto">
            <li class="nav-item" v-if="authStore.isLoggedIn">
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>

             <li class="nav-item" v-else>
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    </div>
  </header>
</template>


<style>

.header-wrapper {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: calc(100% - 40px);
  min-height: 70px;
  height: auto;
  background-color: rgb(97, 39, 94);
  border-radius: 20px;
  padding: 10px 20px;
  box-shadow: 0 0 12px rgba(0,0,0,0.1);
  z-index: 1000;
}

.nav-link{
  color: white;
}

.nav-link:hover {
  color: #ffd6ff;
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 5px;
}

</style>
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
            <li class="nav-item mx-3">
              <RouterLink to="/" class="nav-link active">About Us</RouterLink>
            </li>
            <li class="nav-item mx-3">
              <RouterLink class="nav-link" to="">Community Guidelines</RouterLink>
            </li>
            <li class="nav-item mx-3">
              <RouterLink class="nav-link" to="">My Profile</RouterLink>
            </li>
             <li class="nav-item mx-3">
              <RouterLink class="nav-link" to="">Search Profiles</RouterLink>
            </li>
          </ul>

          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <RouterLink class="nav-link" to="">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

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
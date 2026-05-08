<script setup>
defineProps({
  user: {
    type: Object,
    required: true
  },

  message: {
    type: Object,
    required: true
  }
})

</script>


<template>

  <div :class="['bubble', is_current_user ? 'mine': 'theirs']">
    <div class="person">
      <div class="img">
        <img :src = "user.photo" alt = "profile picture">
      </div>
      <p>{{ user.f_name }}  {{ user.l_name }}</p>
      <p>{{ message.timestamp }}</p>
    </div>
    <div class="content">
      <p>{{ message.content }} </p>
    </div>
  </div>
  </template>



<style>
</style>
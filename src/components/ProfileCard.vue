<script setup>

defineProps({
  user: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class = "card">
            <div class = "imgContainer">
                <img :src = "user.photo" alt = "profile picture"/>
            </div>
            <div class = "card-title">
                <p>{{ user.f_name }} {{ user.l_name }}, {{ user.age }}</p>
            </div>      
            <div class = "card-body">
                <p class = "card-subtitle text-muted">@{{ user.username }}</p>
                <p>{{ user.gender }}</p>
                <p>{{ user.location }}</p>
                <p v-if="user.percentage">{{ user.percentage }}%</p>
            </div>
            <div class="interaction">
                <slot></slot>
            </div>
        </div>
  </template>

  <style>

  .card{
        padding: 20px;
        align-items: center;
        display: flex;
        flex-direction: column;
        justify-content: center;

        max-width: 100%;
        box-sizing: border-box;
        overflow: hidden;     
    }

    .card-body p{
        margin-bottom: 5px;
    }

    .card-subtitle{
        font-size: 14px;
        padding-top: 0px;
    }
    .card-title{
        font-weight: bold;
        margin-bottom: -10px;
    }

    .card-body, .card-title {
        text-align: center;
        width: 100%;
        overflow-wrap: break-word;
    }


    .imgContainer img {
        width: 100%;
        max-width: 150px;   /* adjust as needed */
        height: auto;
        border-radius: 10px;
        object-fit: cover;
    }

    a:hover{
        background-color: red;

    }


</style>
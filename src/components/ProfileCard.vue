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
        
            <RouterLink :to="`/profile/${user.user_ID }`" >@{{ user.username }}</RouterLink>
            <p>{{ user.gender }}</p>
            <p>{{ user.location }}</p>
            <p><i >"{{ user.bio }}"</i></p>
            <p v-if="user.percentage">{{ user.percentage }}%</p>
        </div>        
    
        <div class="interaction">
            <slot></slot>
        </div>
    </div>

  </template>

<style scoped>
    .container{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        width: 100%;
        margin: 0 auto;
    }

    @media (min-width: 1024px) {
    .container {
        grid-template-columns: repeat(3, 1fr);
    }
}

a{
    text-decoration: none;
    color: grey;
    margin:0;
    padding:0;
}

a:hover{
    color: pink;

}

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

    .card-body p i{
        display: -webkit-box;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
        overflow: hidden;
        max-height: 200px;
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


</style>
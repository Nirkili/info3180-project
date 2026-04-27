<script setup>
import { ref, onMounted, resolveComponent } from 'vue';
import { errorMessages } from 'vue/compiler-sfc';

let csrf_token = ref("");
let sucessMessage = ref("");
let errorMessage = ref("");
let matchList = ref([])

let message = ref("Hello World! This is a VueJS and Flask Starter Template.")

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

function loadMatches(){

  fetch('/api/v1/matches',{
    method:'GET',
    headers: {'X-CSRFToken': csrf_token.value,}
  })

  .then(function(response){
    console.log("Status", response);
    if(!response.ok){
      throw new Error(`Server Error: ${response.status}`)
    }

    return response.json()
  })

  .then(function(data){
    matchList.value = data
    console.log(matchList)
    
  })

  .catch(function(error){
    errorMessage.value = error.message;

})

}

onMounted(() => {
  getCsrfToken()
  loadMatches()
})

</script>



<template>
    <div class="container">
      <div v-for= "m in matchList" :key = m.user_ID class = "card">
            <div class = "imgContainer">
                <img :src = "m.photo" alt = "profile picture"/>
            </div>
            <div class = "card-title">
                <p>{{ m.f_name }} {{ m.l_name }}, {{ m.age }}</p>
            </div>      
            <div class = "card-body">
                <p class = "card-subtitle text-muted">@{{ m.username }}</p>
                <p>{{ m.gender }}</p>
                <p>{{ m.location }}</p>
                <p>{{ m.percentage }}%</p>
            </div>
            <div class="interaction">
                <a><i class="fa-solid fa-thumbs-up"></i> Like</a>
                <a><i class="fa-solid fa-thumbs-down"></i> Pass</a>

            </div>
        </div>
    </div>
</template>

<style>

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

/* Add any component specific styles here */
</style>
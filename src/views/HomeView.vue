<script setup>
import { ref, onMounted, /*resolveComponent*/ } from 'vue';
//import { errorMessages } from 'vue/compiler-sfc';
import ProfileCard from '@/components/ProfileCard.vue';

let csrf_token = ref("");
let sucessMessage = ref("");
let errorMessage = ref("");
let matchList = ref([])
let match = ref(false)
let showMatch = ref(false)
let sortOrder = ref('desc')

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

  fetch(`/api/v1/matches?sort=${sortOrder.value}`,{
    method:'GET',
    headers: {'Content-Type': 'application/json'}
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

async function rateUser(userID, type){
    console.log(type)
    
    fetch(`/api/v1/users/${userID}/interaction`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token.value
        },
        body: JSON.stringify({type: type})
    })

    .then(function(response){
        return response.json()
    })

    .then(function(data){
        console.log('matched:', data.matched)
        // Remove card fromthe list
        matchList.value = matchList.value.filter(m => m.user_ID !== userID)

        if(data.matched){
            showMatch.value = true;
            setTimeout(() => showMatch.value = false, 3000)
        }
    })
}

onMounted(() => {
  getCsrfToken()
  loadMatches()
})

</script>



<template>
    <div class="container">
        <div v-if="showMatch" class="match-notification">
            It's a Match!
        </div>

        <div class="filter-container">
          <select v-model="sortOrder" @change="loadMatches">
            <option value="desc">Best Matches</option>
            <option value="asc">Worst Matches</option>
          </select>
        </div>

      <div v-for= "m in matchList" :key ="m.userID">
        <ProfileCard :user="m">
            <a @click="rateUser(m.user_ID, 'Like')"><i class="fa-solid fa-thumbs-up"></i> Like</a>
            <a @click="rateUser(m.user_ID, 'Pass')"><i class="fa-solid fa-thumbs-down"></i> Pass</a>

        </ProfileCard>
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

    .match-notification {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: green;
    color: white;
    padding: 20px;
    border-radius: 10px;
    font-size: 24px;
    z-index: 9999;
}

/* Add any component specific styles here */
</style>
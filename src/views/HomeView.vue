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

  fetch(`/api/v1/home?sort=${sortOrder.value}`,{
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
    
    fetch(`/api/v1/home/${userID}`, {
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

  <div v-if="showMatch" class="match-notification">
            It's a Match!
        </div>

  <div class="sorts">
          <select class="sort" v-model="sortOrder" @change="loadMatches">
            <option value="desc">Best Matches</option>
            <option value="asc">Worst Matches</option>
          </select>
        </div>

    <div class="user-lst-container">
        
      <div v-for= "m in matchList" :key ="m.userID">
        <ProfileCard :user="m">
          <div class="buttons">
            <a @click="rateUser(m.user_ID, 'Like')" class="Like"><i class="fa-solid fa-thumbs-up"></i></a>
            <a @click="rateUser(m.user_ID, 'Pass')" class="Pass"><i class="fa-solid fa-thumbs-down"></i> </a>

          </div>
            
        </ProfileCard>
        </div>
    </div>
</template>

<style scoped>

.main-content{
  justify-content: center;
}


   .sort{
        border-radius: 5px;
        padding: 10px;
        color: #4a154b;
        background-color: white;
        margin-bottom: 30px;
        display:flex;
        justify-content: center;
        width: 150px;
    }




 .user-lst-container{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        width: 100%;
        margin: 0 auto;
    }


  .match-notification {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #4a154b;
    color: white;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #E95DA1;
    font-size: 20px;
    z-index: 9999;
}


.buttons{
  display: flex;
  flex-direction: row;
  gap: 50px;
}

.Like, .Pass{
  color: #4a154b;
  font-size: 25px;
    text-decoration: none;
  }

  .Like:hover, .Pass:hover{
  background-color:  #E95DA1;
  cursor:pointer;
  padding: 2px;
  border-radius:10px;
  }

/* Add any component specific styles here */
</style>
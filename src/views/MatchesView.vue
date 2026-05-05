<script setup>
  import { ref, onMounted } from 'vue';
  import ProfileCard from '@/components/ProfileCard.vue';
  import { useRouter } from 'vue-router';

  const router = useRouter();

  let matches = ref([]);

  function getMatches(){
    fetch('/api/v1/matches', {
      method:'GET',
      headers: {'Content-Type': 'application/json'}
    })

    .then(response => response.json())
    
    .then(function(data) {
       if (Array.isArray(data)){
        matches.value = data
        console.log(data)
    } 
    else {
        matches.value = []
    }
    })

    .catch(function (error) { 
            console.log(error); 
        }); 
  }

  async function messageUser(user_ID){
    const response = await fetch('/api/v1/chats', {
      method: 'GET'
    })

    const data = await response.json();
    const chat = data.chats.find(c => c.matched_user_ID == user_ID)

    if(chat){
      router.push({
        name: 'chats', 
        query:{
          chat_ID: chat.chat_ID
        } 
      })
    }
    
  }

  onMounted(() => {
      getMatches();
    });






</script>
<template>
  <div id="heading">
    Matched Profiles
  </div>


  <div class="matches-container" v-if="matches.length > 0">

    <div v-for="m in matches" :key = "m.userID">
      <ProfileCard :user="m">
        <a @click="messageUser(m.user_ID)">Message</a>
      </ProfileCard>

    </div>


  </div>

  <div v-else id = "no-matches">
        <p>Damn.</p>
    </div>
</template>

<style scoped>

.main-content{
  background-color: white;
}


#heading{
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    color: white;
    padding: 15px;
  }

.matches-container{

    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    width: 100%;
    margin: 0 auto;
    
  }

  #no-matches{
      display: flex;
      justify-content: center;
      align-items: center;
      color: grey;
      height: 60vh;
  }

</style>
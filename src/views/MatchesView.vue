<script setup>
  import { ref, onMounted } from 'vue';
  import ProfileCard from '@/components/ProfileCard.vue';
  import { useRouter } from 'vue-router';

  const router = useRouter();

  let matches = ref([]);

  function getMatches(){
    fetch('/api/v1/user/matches', {
      method:'GET',
      headers: {'Content-Type': 'application/json'}
    })

    .then(response => response.json())
    
    .then(function(data) {
       if (Array.isArray(data)){
        matches.value = data
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
  <div class="matches-container">

    <div v-for="m in matches" :key = "m.userID">
      <ProfileCard :user="m">
        <a @click="messageUser(m.user_ID)">Message</a>
      </ProfileCard>

    </div>


  </div>
</template>

<style scoped>

.main-content{
  background: white;
}

</style>
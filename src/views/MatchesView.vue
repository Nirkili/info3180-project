<script setup>
  import { ref, onMounted } from 'vue';
  import ProfileCard from '@/components/ProfileCard.vue';

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

  onMounted(() => {
      getMatches();
    });






</script>
<template>
  <div class="matches-container">

    <div v-for="m in matches" :key = "m.userID">
      <ProfileCard :user="m">
        <a>Message</a>
      </ProfileCard>

    </div>


  </div>
</template>

<style scoped>

.main-content{
  background: white;
}

</style>
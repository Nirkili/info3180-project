<template>
  <div id = "heading">
    <h1>Bookmarked Profiles</h1>
  </div>
  <div id = "bookContainer" v-if="profiles.length > 0">
      <div v-for="profile in profiles" :key="profile.profile_ID">
        <ProfileCard :user = "profile">
          <a @click="removebookmark(user.profile_ID)"><i class="bi bi-bookmark-fill">Remove from Bookmarks</i></a>
        </ProfileCard>
      </div>
  </div>
  <div id= "noBook" v-else>
    <p>No bookmarks added as yet.</p>
  </div>
</template>

<script setup>
  import {ref, onMounted} from 'vue';
  import ProfileCard from '../components/ProfileCard.vue';

  const profiles = ref([]);
  const csrf_token = ref('');

  onMounted(async () =>{
    await getCsrfToken();
    fetchBookmarked();
  })

  function removebookmark(profile_ID){

    if (!window.confirm("Are you sure you want to remove this bookmark?")) {
      return; 
    }

    fetch(`/api/v1/user/bookmarks/${profile_ID}`, {
        method: 'DELETE',
        headers:{'X-CSRFToken': csrf_token.value,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then (function (data) { 
        console.log(data);
        fetchBookmarked();
    }) 
    .catch(function (error) { 
        console.log(error); 
    }); 

    };
  

  function fetchBookmarked(){
    fetch('/api/v1/user/bookmarks', {
        method: 'GET'
    })
    .then(response => response.json())
    .then (function (data) { 
        profiles.value = data; 
    }) 
    .catch(function (error) { 
        console.log(error); 
    }); 
  }

  function getCsrfToken() {
    return fetch('/api/v1/csrf-token')
      .then((response) => response.json())
      .then((data) => {

        csrf_token.value = data.csrf_token
      })
      .catch((error) => {
        console.log(error)
      })
    }
</script>

<style>

  #heading{
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    color: white;
    padding: 15px;
  }
  #bookContainer{

    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    width: 100%;
    margin: 0 auto;
    
  }

  #noBook{
      display: flex;
      justify-content: center;
      align-items: center;
      color: grey;
      height: 60vh;
  }

  .interaction{
        color: #E95DA1;
    }

  .interaction:hover{
      color: #4a154b;
      cursor: pointer;
  }

</style>
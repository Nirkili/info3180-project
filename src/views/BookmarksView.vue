<template>
  <div id = "heading">
    <h1>Bookmarked Profiles</h1>
  </div>
  <div id = "bookContainer">
    <div v-if="profiles.length > 0">
      <div class = "card" v-for="profile in profiles" :key="profile.profile_ID">
         <div class = "imgContainer">
                <img :src = "profile.photo" alt = "profile picture"/>
          </div>
          <div class = "card-title">
              <p>{{ profile.first_name }} {{ profile.last_name }}, {{ profile.age }}</p>
          </div>      
          <div class = "card-body">
              <p class = "card-subtitle text-muted">@{{ profile.user_name }}</p>
              <p>{{ profile.gender }}</p>
              <p>{{ profile.location }}</p>
          </div>
          <div>
            <button id = "removeButton">Remove Bookmark</button>
          </div>
      </div>
    </div>
    <div id= "noBook" v-else>
      <p>No bookmarks added as yet.</p>
    </div>
  </div>
</template>

<script setup>
  import {ref, onMounted} from 'vue'

  const profiles = ref([]);

  onMounted(() =>{
    fetchBookmarked()
  })

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
  .card{
      padding: 10px;
      align-items: center;
      display: flex;
      flex-direction: column;
      justify-content: center;
      overflow-y: auto;
      width: 50%;
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

  #noBook{
      display: flex;
      justify-content: center;
      align-items: center;
      color: grey;
      height: 60vh;
  }

</style>
<script setup>
  //Imports the ref and onMounted functions from Vue and the ProfileCard component.
  import {ref, onMounted} from 'vue';
  import ProfileCard from '../components/ProfileCard.vue';

  const profiles = ref([]);
  const csrf_token = ref('');
  const message = ref('');
  const removed = ref(false);

  //When the component is mounted, the CSRF token is retrieved and stored first and then fetchBookmarked function is called to display all bookmarked profiles.
  onMounted(async () =>{
    await getCsrfToken();
    fetchBookmarked();
  })

  //Function to remove a profile from bookmarks. Accepts the profileID of the user to be removed from bookmarks.
  function removebookmark(profile_ID){

    //Confirmation prompt to confirm if the user really wants to remove the bookmark.
    if (!window.confirm("Are you sure you want to remove this bookmark?")) {
      return; 
    }

    //Deletes the bookmark from the database and then calls fetchBookmarked to refresh the list of bookmarked profiles displayed.
    fetch(`/api/v1/bookmarks/${profile_ID}`, {
        method: 'DELETE',
        headers:{'X-CSRFToken': csrf_token.value,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then (function (data) { 
        console.log(data);
        fetchBookmarked();

        if(data.removed){
            message.value = data.message;
            removed.value = data.removed;
            setTimeout(() => removed.value = false, 3000)
        }
    }) 
    .catch(function (error) { 
        console.log(error); 
    }); 

    };
  
  //Function to fetch the list of bookmarked profiles from the server and store it in the profiles variable.
  function fetchBookmarked(){
    fetch('/api/v1/bookmarks', {
        method: 'GET'
    })
    .then(response => response.json())
    .then (function (data) { 
        profiles.value = data; 
    }) 
    .catch(function (error) { 
        console.log(error); 
    }); 
  };

  //Function to get the CSRF token from the server which is required to make POST and DELETE requests. The token is stored in the csrf_token variable.
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



<template>
  <div v-if= "removed" class="alert alert-success" role="alert">
            {{message}}
  </div>
  

  <div id = "heading">
    <h1>Bookmarked Profiles</h1>
  </div>


  <!--Loops through the bookmarked profiles and displays them-->
  <div class = "book-container" v-if="profiles.length > 0">
      <div v-for="profile in profiles" :key="profile.profile_ID">
        <ProfileCard :user = "profile">
          <!--Adds option to remove from bookmarks-->
          <a class="bookmark" @click="removebookmark(profile.profile_ID)"><i class="bi bi-bookmark-fill">Remove Bookmark</i></a>
        </ProfileCard>
      </div>
  </div>


  <div id= "no-book" v-else>
    <p>No bookmarks added as yet.</p>
  </div>


</template>


<style scoped>

  .main-content{
        background-color: none;
    }

  #heading{
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    color: white;
    padding: 15px;
  }
  .book-container{

    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    width: 100%;
    margin: 0 auto;
    
  }

  #no-book{
      display: flex;
      justify-content: center;
      align-items: center;
      color: grey;
      height: 60vh;
  }
  .alert {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #E95DA1;
    color: white;
    padding: 20px;
    border-radius: 10px;
    z-index: 9999;
}

  .bookmark{
        color: #E95DA1;
        text-decoration: none;
    }

    .bookmark:hover{
      color: #4a154b;
      cursor: pointer;
  }


</style>

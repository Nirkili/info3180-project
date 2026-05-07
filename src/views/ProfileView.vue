<<<<<<< HEAD
<script setup>
  import { ref, onMounted, watch} from 'vue';
  import { useRouter, useRoute } from 'vue-router';


  const router = useRouter();
  const route = useRoute();
  const profile = ref(null);
  let matches = ref([]);




  function getMatches(){
    fetch('/api/v1/matches', {
      method:'GET',
      headers: {'Content-Type': 'application/json',}
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


  function getMyProfile(){
    profile.value = null;
    
    fetch('/api/v1/profile/me', {
        method :'GET',
        headers : {
          'Content-Type': 'application/json'
        }
  })

  .then(response => response.json())
  .then(function(data){
    profile.value = data;
    console.log(data)
  })

  .catch(function(error){
    console.log(error)
  })


  }

  function getProfile(){
    profile.value = null

    fetch(`/api/v1/profile/${route.params.id}`,{
              method : 'GET',
              headers : {
                'Content-Type': 'application/json'
              }

        })

          .then(response => response.json())
          .then(function(data){
            profile.value = data;
          })

          .catch(function(error){
            console.log(error)
          })

  }

  // Remove the onMounted and replace with this
watch(
  () => route.params.id,
  () => {
    if (route.params.id) {
      getProfile()
    } else {
      getMyProfile()
      getMatches()
    }
  },
  { immediate: true }  // ← runs on initial load too
)


</script>


<template>
  <div class="profile-container" v-if="profile" :class="{'is-my-profile': !route.params.id}">
    
    
     <div class="left-column">
      <div class="profile">
        <div class="img"></div>
        <div class="details">
          <div class="top">
            <h2>{{ profile.first_name }} {{ profile.last_name }}, {{ profile.age }}</h2>
            <p><i class="fa-solid fa-location-dot"></i> {{ profile.location }}</p>
          </div>
          <div class="bio">{{ profile.bio }}</div>
          <div class="interests">
            <span class="interest" v-for="interest in profile.interests" :key="interest">
              {{ interest }}
            </span>
          </div>
        </div>
      </div>

      <div class="photos">
        <h3>Photos</h3>
        <div class="images"></div>
      </div>

      <div class="preferences">
        <h3>About</h3>
        <div id="children">Family plans: {{ profile.wants_children }}</div>
        <div id="age-preference">Age preference: {{  profile.age_preference }} </div>
        <div id="education">Education: {{ profile.education }}</div>
        <div id="relationship-status">Status: {{ profile.relationship_status }}</div>
        <div id="career">Works as: {{ profile.job }}</div>
      </div>
    </div>
    

    <div class="matches-container" v-if="matches.length > 0">
      <h3>Matches</h3>

      <div v-for="m in matches" :key = "m.userID">
        <div class="match">
          <div class="m-img">
              <img :src = "m.photo" alt = "profile picture"/>
          </div>
          <div class="info">
            <p>{{ m.f_name }} {{ m.l_name }}, {{ m.age }}</p>
            <p>{{ m.username }}</p>
          </div>
        </div>
      
        <a @click="messageUser(m.user_ID)">Message</a>

    </div>
  </div>

  <div v-else id = "no-matches-container">
        <p>Damn.</p>
    </div>



  </div>
</template>



<style scoped>

.profile-container{
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  padding: 0;
  width: 100%;
  margin: 0 auto;
  border-radius: 20px;
}

.left-column{
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile{
  display: flex;
  flex-direction: row;
  gap: 20px;
  background-color: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06)
}

.matches-container{
  display: none;
}

.is-my-profile .matches-container{
  display: block;
  background-color: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.details{
  flex:1;
  display: flex;
  flex-direction: column;
  gap:10px;
}

.interests{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.interest{
  background-color: #E95DA1;
  color: white;
  border: 1px solid #f5c0cc;
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 0.85rem;

}

.photos{
  background-color: white;border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06)

}

.preferences{
  background-color: white;border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06)
}

=======
<script setup>
  import { ref, onMounted, watch} from 'vue';
  import { useRouter, useRoute } from 'vue-router';


  const router = useRouter();
  const route = useRoute();
  const profile = ref(null);
  let matches = ref([]);




  function getMatches(){
    fetch('/api/v1/matches', {
      method:'GET',
      headers: {'Content-Type': 'application/json',}
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


  function getMyProfile(){
    profile.value = null;
    
    fetch('/api/v1/profile/me', {
        method :'GET',
        headers : {
          'Content-Type': 'application/json'
        }
  })

  .then(response => response.json())
  .then(function(data){
    profile.value = data;
    console.log(data)
  })

  .catch(function(error){
    console.log(error)
  })


  }

  function getProfile(){
    profile.value = null

    fetch(`/api/v1/profile/${route.params.id}`,{
              method : 'GET',
              headers : {
                'Content-Type': 'application/json'
              }

        })

          .then(response => response.json())
          .then(function(data){
            profile.value = data;
          })

          .catch(function(error){
            console.log(error)
          })

  }

  // Remove the onMounted and replace with this
watch(
  () => route.params.id,
  () => {
    if (route.params.id) {
      getProfile()
    } else {
      getMyProfile()
      getMatches()
    }
  },
  { immediate: true }  // ← runs on initial load too
)


</script>


<template>
  <div class="profile-container" v-if="profile" :class="{'is-my-profile': !route.params.id}">
    
    
     <div class="left-column">
      <div class="profile">
        <div class="img"></div>
        <div class="details">
          <div class="top">
            <h2>{{ profile.first_name }} {{ profile.last_name }}, {{ profile.age }}</h2>
            <p><i class="fa-solid fa-location-dot"></i> {{ profile.location }}</p>
          </div>
          <div class="bio">{{ profile.bio }}</div>
          <div class="interests">
            <span class="interest" v-for="interest in profile.interests" :key="interest">
              {{ interest }}
            </span>
          </div>
        </div>
      </div>

      <div class="photos">
        <h3>Photos</h3>
        <div class="images"></div>
      </div>

      <div class="preferences">
        <h3>About</h3>
        <div id="children">Family plans: {{ profile.wants_children }}</div>
        <div id="age-preference">Age preference: {{  profile.age_preference }} </div>
        <div id="education">Education: {{ profile.education }}</div>
        <div id="relationship-status">Status: {{ profile.relationship_status }}</div>
        <div id="career">Works as: {{ profile.job }}</div>
      </div>
    </div>
    

    <div class="matches-container" v-if="matches.length > 0">
      <h3>Matches</h3>

      <div v-for="m in matches" :key = "m.userID">
        <div class="match">
          <div class="m-img">
              <img :src = "m.photo" alt = "profile picture"/>
          </div>
          <div class="info">
            <p>{{ m.f_name }} {{ m.l_name }}, {{ m.age }}</p>
            <p>{{ m.username }}</p>
          </div>
        </div>
      
        <a @click="messageUser(m.user_ID)">Message</a>

    </div>
  </div>

  <div v-else id = "no-matches-container">
        <p>Damn.</p>
    </div>



  </div>
</template>



<style scoped>

.profile-container{
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  padding: 0;
  width: 100%;
  margin: 0 auto;
  border-radius: 20px;
}

.left-column{
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile{
  display: flex;
  flex-direction: row;
  gap: 20px;
  background-color: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06)
}

.matches-container{
  display: none;
}

.is-my-profile .matches-container{
  display: block;
  background-color: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.details{
  flex:1;
  display: flex;
  flex-direction: column;
  gap:10px;
}

.interests{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.interest{
  background-color: #E95DA1;
  color: white;
  border: 1px solid #f5c0cc;
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 0.85rem;

}

.photos{
  background-color: white;border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06)

}

.preferences{
  background-color: white;border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06)
}

>>>>>>> origin/Jaden
</style>
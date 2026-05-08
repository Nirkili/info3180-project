<script setup>
  import { ref, onMounted, watch} from 'vue';
  import { useRouter, useRoute } from 'vue-router';


  let csrf_token = ref("");
  const router = useRouter();
  const route = useRoute();
  const profile = ref(null);
  let matches = ref([]);
  const isEditing = ref(false)
  const editForm = ref({})



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
    console.log(profile.interests)
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

  function editProfile(){
    editForm.value = {...profile.value};
    isEditing.value = true;
  }

  async function saveProfile(){
    const form = new FormData();

    form.append('bio', editForm.value.bio);
    form.append('location', editForm.value.location);
    form.append('gender_preference', editForm.value.gender_preference);
    form.append('gender', editForm.value.gender)
    form.append('age_preference', editForm.value.age_preference);
    form.append('wants_children', editForm.value.wants_children);
    form.append('visibility_status', editForm.value.visibility_status);
    form.append('job', editForm.value.job);
    form.append('education', editForm.value.education);
    form.append('relationship_status', editForm.value.relationship_status);
    form.append('relationship_type_preference', editForm.value.relationship_type_preference);

    fetch('/api/v1/profile', {
      method: 'PUT',
      credentials: 'include',
      headers:{
      'X-CSRFToken': csrf_token.value,
      } ,
      body: form
    })

    .then(response => response.json())
    .then(function(data){
      profile.value = {...profile.value, ...editForm.value};
      isEditing.value = false;
    })

    .catch(function(error){
      console.log(error)
    });
  }


  

  // Remove the onMounted and replace with this
watch(
  () => route.params.id,
  () => {
    if (route.params.id) {
      getProfile()
      getCsrfToken();
    } else {
      getMyProfile()
      getMatches()
       getCsrfToken();
    }
  },
  { immediate: true }  // ← runs on initial load too
)


</script>


<template>
  <div v-if="profile" class="profile-container" :class="{'is-my-profile': !route.params.id}">

    <div class="left-column">

      <div class="profile">
        <div class="img"></div>
        <div class="details">
          <div class="top">

            <h2>{{ profile.first_name }} {{ profile.last_name }}, {{ profile.age }}</h2>

            <p v-if="!isEditing"><i class="fa-solid fa-location-dot"></i> {{ profile.location }}</p>
            <div v-else>
              <i class="fa-solid fa-location-dot"></i>
              <select v-model="editForm.location">
                <option value="Kingston">Kingston</option>
                <option value="St. Andrew">St. Andrew</option>
                <option value="St. Thomas">St. Thomas</option>
                <option value="Portland">Portland</option>
                <option value="Trelawny">Trelawny</option>
                <option value="Clarendon">Clarendon</option>
                <option value="Manchester">Manchester</option>
                <option value="St. Elizabeth">St. Elizabeth</option>
                <option value="Westmoreland">Westmoreland</option>
                <option value="Hanover">Hanover</option>
                <option value="St. Mary">St. Mary</option>
                <option value="St. Ann">St. Ann</option>
                <option value="St. James">St. James</option>
              </select>
            </div>

            <div v-if="!isEditing">
              <div><i>"{{ profile.bio }}"</i></div>
              <div id="status">{{ profile.visibility_status }}</div>
            </div>
            <div class="bio" v-else>
              <textarea v-model="editForm.bio" placeholder="Write about you!"></textarea>
              <select v-model="editForm.visibility_status">
                <option value="Public">Public</option>
                <option value="Private">Private</option>
              </select>
            </div>

            <div class="interests">
              <span class="interest" v-for="interest in profile.interests" :key="interest">
                {{ interest }}
              </span>
            </div>

           
          </div>
        </div>
      </div>

      <div class="preferences">
        <h3>About</h3>

        <div v-if="!isEditing" class=prefs>
          <div class="p-item"><strong>Gender</strong>: {{ profile.gender }}</div>
          <div class="p-item"><strong>Prefers</strong>: {{ profile.gender_preference }}</div>
          <div class="p-item"><strong>Family plans</strong>: {{ profile.wants_children }}</div>
          <div class="p-item"><strong>Age preference</strong>: {{ profile.age_preference }}</div>
          <div class="p-item"><strong>Relationship Status</strong>: {{ profile.relationship_status }}</div>
          <div class="p-item"><strong>Looking For</strong>: {{ profile.relationship_type_preference }}</div>
          <div class="p-item"><strong>Education</strong>: {{ profile.education }}</div>
          <div class="p-item"><strong>Works as</strong>: {{ profile.job }}</div>
           <button class="btn btn-custom" v-if="!route.params.id && !isEditing" @click="editProfile">
              Edit Profile
            </button>

        </div>

        <div v-else>
          <div><strong>Gender</strong>:
            <select v-model="editForm.gender">
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Non-binary">Non-binary</option>
            </select>
          </div>

          <div><strong>Gender Preference</strong>:
            <select v-model="editForm.gender_preference">
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Non-binary">Non-binary</option>
            </select>
          </div>

          <div><strong>Family plans</strong>:
            <select v-model="editForm.wants_children">
              <option value="Wants Children">Wants Children</option>
              <option value="Does Not Want Children">Does Not Want Children</option>
            </select>
          </div>

          <div><strong>Age preference</strong>:
            <select v-model="editForm.age_preference">
              <option value="18-24">18-24</option>
              <option value="25-29">25-29</option>
              <option value="30-40">30-40</option>
              <option value=">40">>40</option>
            </select>
          </div>

          <div><strong>Relationship Status</strong>:
            <select v-model="editForm.relationship_status">
              <option value="Single">Single</option>
              <option value="Open Relationship">Open Relationship</option>
              <option value="Married">Married</option>
            </select>
          </div>

          <div><strong>Looking For</strong>:
            <select v-model="editForm.relationship_type_preference">
              <option value="Casual">Casual</option>
              <option value="Serious">Serious</option>
            </select>
          </div>

          <div><strong>Education</strong>:
            <input type="text" v-model="editForm.education" placeholder="e.g., Bachelor's Degree" />
          </div>

          <div><strong>Works as</strong>:
            <input type="text" v-model="editForm.job" placeholder="e.g., Software Engineer" />
          </div>

          <div class="btn-group">
            <button class="btn btn-custom" @click="saveProfile">Save Profile</button>
            <button class="btn btn-cancel" @click="isEditing = false">Cancel</button>
          </div>
        </div>

      </div>

    </div>

    <div class="right">
      <div class="matches-container" v-if="!route.params.id">
        <h3>Matches</h3>

        <div v-if="matches.length > 0">
          <div v-for="m in matches" :key="m.user_ID" class="match">
            <div class="m-img">
              <img :src="m.photo" alt="profile picture" />
            </div>
            <div class="info">
              <p><strong>{{ m.f_name }} {{ m.l_name }}, {{ m.age }}</strong></p>
              <RouterLink :to="`/profile/${m.user_ID}`">@{{ m.username }}</RouterLink>
            </div>
            <div class="match-actions">
              <a @click="messageUser(m.user_ID)">Message</a>
            </div>
          </div>
        </div>

        <div v-else>
          <p>No matches?. Let's find some love!</p>
        </div>

      </div>
    </div>

  </div>
</template>



<style scoped>

.bio{
  display: flex;
  justify-content: space-between;
}

.p-item{
  font-weight: 600px;

}

.bio select{
  margin-left: 20px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

textarea{
  width: 50%;
  height: 100px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.matches-container{
  display: none;
}

.is-my-profile .matches-container{
  display: flex;
  flex-direction: column;
  gap: 12px;
  background-color: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
   overflow-y: auto;
}

.match{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  border-radius: 10px;
  background-color: #fbf7fc;
  padding: 12px;
  border: 0.5px solid purple
}

.details{
  flex:1;
  display: flex;
  flex-direction: column;
  gap:10px;
}

#status{
  background-color: #4a154b;
  font-weight: bold;
  margin-top: 10px;
  padding: 15px;
  border: none;
  border-radius: 25px;
  color: white;
  width: fit-content;
  margin-bottom: 20px;
}

.interests{
  display: flex;
  flex-wrap: wrap;
}

.interest{
  background-color: #E95DA1;
  color: white;
  border: 1px solid #f5c0cc;
  border-radius: 20px;
  padding: 10px;
  margin-right: 10px;
  font-size: 0.85rem;

}

.photos{
  background-color: white;border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06)

}

.preferences, .top{
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06)
}

.preferences select, .preferences input, .top select{
  width: 50%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-top: 10px;
}

.btn-group{
  display: flex;
  gap: 10px;
  flex-direction: row;
}
.btn{
  margin-top: 20px;
  width: 120px;
  padding: 10px;
  border: none;
  border-radius: 20px;
  background-color: #4a154b;
  color: white;
}

.btn:hover{
  background-color: #E95DA1;
  cursor: pointer;
}

.p-item{
  margin-bottom: 5px;
}

.prefs{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px 20px;
}

a{
    text-decoration: none;
    color: grey;
    margin:0;
    padding:0;
}

a:hover{
    color: rgb(182, 99, 113);

}

</style>
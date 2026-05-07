<script setup>
// Functionality for interests selection

import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

// Declaration of reactive variables
let csrf_token = ref("")
let interests = ref([])
let selected = ref([])
let error = ref("")

// Fetches all interests, and CSRF Token when the page loads
onMounted(() => {
  fetch("/api/v1/csrf-token", {
  credentials: "include"
  })
    .then(res => res.json())
    .then(data => {
      csrf_token.value = data.csrf_token
    })

  fetch("/api/v1/interests", {
    credentials: "include"
  })
    .then(res => res.json())
    .then(data => {
      interests.value = data
    })
})

// Manages the selection and deselection of interests by the user
function toggleInterest(id) {
  if (selected.value.includes(id)) {
    selected.value = selected.value.filter(i => i !== id)
  } else {
    if (selected.value.length >= 5) return
    selected.value.push(id)
  }
}

// Updates whenever there is a change with selected interests
const isValid = computed(() => {
  return selected.value.length >= 3 && selected.value.length <= 5
})

// Submits the user's interests once the criteria is met
function submitInterests() {
  if (!isValid.value) {
    error.value = "Please select 3–5 interests"
    return
  }

  // Sends submitted selections to the backend to be committed to the database
  fetch("/api/v1/profile/interest", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token.value  
    },
    credentials: "include",
    body: JSON.stringify({
      interest_ids: selected.value
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        error.value = data.error // Error message if there is an issue
      } else {
        router.push('/home') // Ensures the user is brought to the home screen if successful
      }
    })
}
</script>


<template>
      
  <div class="container">

    <h1>What interests you?</h1>

    <h5>Select 3 - 5 of the interests below</h5>

    <div class="interests">
      
      <!-- Creates a button for each interest -->
      <button
        v-for="i in interests"
        :key="i.id"
        type="button"
        @click="toggleInterest(i.id)"
        :class="['interest-btn', { selected: selected.includes(i.id) }]" 
      >                           
        {{ i.name }}
      </button>
    </div>

    <!-- Displays any error if one occurs -->
    <p v-if="error">{{ error }}</p>

    <!-- Ensures submission can only be done when at least 3 interests are selected -->
    <button
      class="btn btn-secondary"
      :disabled="!isValid"
      @click="submitInterests"
    >
      Submit Interests
    </button>

  </div>

</template>


<style scoped>
h1 {
    padding-top: 20px;
}


.container {
  display: flex;
  flex-direction: column;
  margin-bottom: 80px;
  background-color: white;
  padding: 20px;
  border-radius: 20px;
  align-items: center;
  width: 50%;
}

.interests {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
  width: 100%;
  padding-bottom: 25px;
  padding-top: 15px;
}

button {
    border-radius: 20px;
    background-color: #9a60ab;
    color: white;
    gap: 15px;
}

.interest-btn {
 border-radius: 20px;
    background-color: gray;

    color: white;
    gap: 15px;
};

a {
  color: #9a60ab;
  text-decoration: none;
  font-weight: bold;
}

.interest-btn:hover {
  border-color: #888;
}

.interest-btn.selected {
  background-color: #E95DA1;
  color: white;
  border-color: #E95DA1;
}
</style>
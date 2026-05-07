<script setup>
// Register user functionality

import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

// Declaration of reactive variables
let csrf_token = ref("")
let errorMessages = ref([])
let successMessage = ref("")

// Form fields
let username = ref("")
let first_name = ref("")
let last_name = ref("")
let password = ref("")
let confirmation = ref("") // Confirmation of password
let email = ref("")
let birthdate = ref("")
let gender = ref("")
let gender_preference = ref("")
let relationship_preference = ref("")
let wants_children = ref("")
let age_preference = ref("")
let radius_preference = ref("")
let location = ref("")

// Fetches CSRF Token when the page loads
onMounted(() => {
  getCsrfToken()
})

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(res => res.json())
    .then(data => {
      csrf_token.value = data.csrf_token
    })
    .catch(err => {
      console.log(err)
    })
}

// FORM VALIDATION (prevents empty submission)
const isFormValid = computed(() => {
  return (
    username.value &&
    first_name.value &&
    last_name.value &&
    password.value === confirmation.value &&
    email.value &&
    gender.value &&
    birthdate.value &&
    gender_preference.value &&
    relationship_preference.value &&
    wants_children.value &&
    age_preference.value &&       
    radius_preference.value 
  )
})

// 
function register() {
  errorMessages.value = []

  // Extra safety check
  if (!isFormValid.value) {
    errorMessages.value.push({
      field: "form",
      message: "Please fill in all fields"
    })
    return
  }

  // Creating a new form and adding submitted user information to it
  let form_data = new FormData()

  
  form_data.append('username', username.value)
  form_data.append('first_name', first_name.value)
  form_data.append('last_name', last_name.value)
  form_data.append('password', password.value)
  form_data.append('email', email.value)
  form_data.append("date_of_birth", birthdate.value)
  form_data.append("confirmation", confirmation.value)
  form_data.append('gender', gender.value)
  form_data.append('gender_preference', gender_preference.value)
  form_data.append('relationship_preference', relationship_preference.value)
  form_data.append('wants_children', wants_children.value)
  form_data.append("age_preference", age_preference.value)
  form_data.append("radius_preference", radius_preference.value)
  form_data.append('location', location.value)

  // Sends form to the backend to be committed to the database
  fetch('/api/v1/auth/register_user', {
    method: 'POST',
    body: form_data,
    credentials: 'include',
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }
      return response.json()
    })
    .then(data => {
      if (data.errors) {
        errorMessages.value = data.errors
      } 
      
      else {

        // Set user session
        authStore.setLoggedIn(data.user_id, data.first_name, data.last_name)
        successMessage.value = data.message;
      

        // Store user_id for next step in registration
        localStorage.setItem("user_id", data.user_id)

        // Ensures the user moves to the interests page
        router.push('/register_interest')
      }
    })
    .catch(error => {
      errorMessages.value = [
        { field: "error", message: error.message } // Displays error message if one occurs
      ]
    })
}
</script>

<template>
  <div class="container">

    <h1>Ready to find love?</h1>

    <form @submit.prevent="register">

      <div class="labels">

        <!-- Column 1 -->
        <div class="section">
          <input type="text" v-model="username" placeholder="Username" />
          <input type="text" v-model="first_name" placeholder="First Name" />
          <input type="text" v-model="last_name" placeholder="Last Name" />
          <input type="date" v-model="birthdate" />
          <input type="password" v-model="password" placeholder="Password" />
          <input type="password" v-model="confirmation" placeholder="Confirm Password" />
          <input type="text" v-model="email" placeholder="Email" />
          
        </div>

        <!-- Column 2 -->
        <div class="section">
      
         
            

            <select v-model="gender">
              <option disabled value="">Select Your Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Non-binary">Non-binary</option>
            </select>
         

          <select v-model="location">
            <option disabled value="">Location</option>
              <option value = "Kingston">Kingston</option>
              <option value = "St.Andrew">St.Andrew</option>
              <option value = "St.Thomas">St.Thomas</option>
              <option value = "Portland">Portland</option>
              <option value = "Trelawny">Trelawny</option>
              <option value = "Clarendon">Clarendon</option>
              <option value = "Manchester">Manchester</option>
              <option value = "St.Elizabeth">St.Elizabeth</option>
              <option value = "Westmoreland">Westmoreland</option>
              <option value = "Hanover">Hanover</option>
              <option value = "St.Mary">St.Mary</option>
              <option value = "St.Ann">St.Ann</option>
              <option value = "St.James">St.James</option>
          </select>

          <select v-model="gender_preference">
            <option disabled value="">Select Your Gender Preference</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Non-binary">Non-binary</option>
          </select>

          <select v-model="relationship_preference">
            <option disabled value="">Select Your Relationship Preference</option>
            <option value="Casual">Casual</option>
            <option value="Serious">Serious</option>
          </select>

          <select v-model="wants_children">
            <option disabled value="">Do you want children?</option>
            <option value="Wants Children">Yes</option>
            <option value="Does Not Want Children">No</option>
          </select>

          <select v-model="age_preference">
            <option disabled value="">Select Age Preference</option>
            <option value="18-24">18–24</option>
            <option value="25-29">25–29</option>
            <option value="30-40">30–40</option>
            <option value=">41">41+</option>
          </select>

          <select v-model="radius_preference">
            <option disabled value="">Select Radius</option>
            <option value="25">25 km</option>
            <option value="50">50 km</option>
            <option value="100">100 km</option>
            <option value="250">250 km</option>
          </select>
        </div>

      </div>

      <!-- Only available to click when the form is valid -->
      <button
        type="submit"
        class="btn btn-secondary"
        :disabled="!isFormValid"
      >
        Continue
      </button>

      <!-- Displays the first error message if one occurs -->
      <p v-if="errorMessages.length">
        {{ errorMessages[0].message }}
      </p>

    </form>

    <!-- Link to login for returning users -->
    <p>
      Already have an account?
      <router-link :to="{ name: 'login' }">Login</router-link>
    </p>

  </div>
</template>


<style scoped>
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

.labels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  width: 100%;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

h1 {
  padding-bottom: 15px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 25px;
  align-items: center;
  width: 100%;
  padding-bottom: 15px;
}

input, select {
  border-radius: 20px;
  height: 45px;
  padding: 0 10px;
  width: 100%;
}

button {
  border-radius: 20px;
  background-color: #9a60ab;
  color: white;
  padding: 10px 20px;
}

a {
  color: #9a60ab;
  text-decoration: none;
  font-weight: bold;
}

/* Mobile: stack everything */
@media (max-width: 768px) {
  .labels {
    grid-template-columns: 1fr;
  }

  .row {
    grid-template-columns: 1fr;
  }

  .container {
    width: 90%;
  }
}
</style>
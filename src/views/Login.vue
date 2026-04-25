<script setup>
import {ref, onMounted} from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

  onMounted(() => {
    getCsrfToken();
  })



  let csrf_token = ref("");
  let successMessage = ref("");
  let errorMessages = ref([])
  let email = ref("")
  let password = ref("")

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


function login(){
  let form_data = new FormData()
  form_data.append('email', email.value)
  form_data.append('password', password.value)

  fetch('/api/v1/auth/login', {
    method: 'POST',
    body: form_data,
    credentials: 'include',
    headers:{
      'X-CSRFToken': csrf_token.value,
    }

  })

  .then(function(response){
    console.log("Status", response);
    if (!response.ok){
      throw new Error(`Server error: ${response.status}`)
    }
    return response.json()
  })

  .then(function(data){
    console.log(data)

    if(data.errors){
      errorMessages.value = data.errors;
    }

    else{
      authStore.setLoggedIn(data.user_id)
      localStorage.setItem("first_name", data.first_name)
      localStorage.setItem("last_name", data.last_name)
      successMessage.value = data.message;
      router.push('/home')
    }
  })

  .catch(function(error){
    errorMessages.value = [{field: 'error', message: error.message}]
  })



}

</script>



<template>
  <div class="container">

    <div class="form-section">
        <h1>Welcome Back!</h1>
        <form @submit.prevent="login" id="login-form">
            <input type="text" required v-model="email" placeholder="  Email">
            <input type="password" required v-model="password" placeholder="  Password">

             <div v-if="errorMessages.length > 0" class="error-messages">
                  <p>Invalid email or password</p>
              </div>

            <button type="submit">Login</button>

            <p>Don't have an account? <router-link :to="{ name: 'register_user' }">Register here!</router-link></p>
        </form>
    </div>

    <div class="image-display">
      <img src="/images/login_image.jpeg">
    </div>

  </div>
</template>




<style scoped>
/*-----Form Heading Design-----*/
h1 {
    padding-bottom: 20px;
}


/*-----Container Design-----*/
.container {
  display: flex;
  width: 100%;
  background: white;
  padding: 20px;
  border-radius: 20px;
}


/*-----Form Designs-----*/
.form-section {
    display: flex;
    flex-direction: column;
    margin-top: 80px;
    margin-bottom: 80px;
    background-color: white;
    padding: 20px;
    border-radius: 20px;
}

form {
    display: flex;
    flex-direction: column;
    gap: 25px;
    align-items: center;
    height: 200%;
}

button {
    width: 30%;
    border-radius: 20px;
    background-color: #9a60ab;
    color: white;
    border: none;
    width: 90px;
    height: 40px;
}

button:hover{
  background-color: #8398d1;
  cursor: pointer;
  transform: translate(0, -2px);
}

input {
    width: 100%;
    border-radius: 12px;
    padding: 12px 15px;
    font-size: 1rem;
    transition: 0.2s ease;
}

input:focus{
   outline: none;
   box-shadow: 0 0 0 3px rgba(154, 96, 171, 0.2);
  
}

a {
  color: #9a60ab;
  text-decoration: none;
  font-weight: bold;
}


/*-----Image Design-----*/
.image-display {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-display img {
  width: 70%;
  height: 70%;
  object-fit: cover;
  border-radius: 20px;

}

.error-messages{
  color: red;
  font-size: 0.9rem;
  text-align: center;
}




</style>
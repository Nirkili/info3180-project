<<<<<<< HEAD
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
      // Set authStore variables
      authStore.setLoggedIn(data.user_id, data.first_name, data.last_name)
      successMessage.value = data.message;

      // Redirect to the homepage on successful login
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

  <!--Carousel-->
  <!--Taken from Bootstrap with the help of W3Schools-->
  <!--https://getbootstrap.com/docs/4.0/components/carousel/-->
  <!--https://www.w3schools.com/bootstrap/bootstrap_carousel.asp-->

  <div id="carousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="3000">

    <!-- Wrapper for slides -->
    <div class="carousel-inner">
      <div class="carousel-item active">
        <img src="/images/login_image.jpeg" class="d-block w-100" alt="Slide 1">
      </div>
      <div class="carousel-item">
        <img src="/images/couplepic.jpg" class="d-block w-100" alt="Slide 2">
      </div>
      <div class="carousel-item">
        <img src="/images/couplepic2.jpg" class="d-block w-100" alt="Slide 3">
      </div>
    </div>

    <!-- Left and right controls -->
    <button class="carousel-control-prev" type="button" data-bs-target="#carousel" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carousel" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
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

/*-----Image Design-----*/
#carousel{
  flex: 1;
  width: 50%;
  overflow: hidden;
  height: 450px;
  padding-left: 40px;
  border-radius: 20px;
}

.carousel-item img {
  width: 50%;
  height: 450px;
  object-fit: cover;
  border-radius: 20px;
}

.error-messages{
  color: red;
  font-size: 0.9rem;
  text-align: center;
}

=======
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
      // Set authStore variables
      authStore.setLoggedIn(data.user_id, data.first_name, data.last_name)
      successMessage.value = data.message;

      // Redirect to the homepage on successful login
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

  <!--Carousel-->
  <!--Taken from Bootstrap with the help of W3Schools-->
  <!--https://getbootstrap.com/docs/4.0/components/carousel/-->
  <!--https://www.w3schools.com/bootstrap/bootstrap_carousel.asp-->

  <div id="carousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="3000">

    <!-- Wrapper for slides -->
    <div class="carousel-inner">
      <div class="carousel-item active">
        <img src="/images/login_image.jpeg" class="d-block w-100" alt="Slide 1">
      </div>
      <div class="carousel-item">
        <img src="/images/couplepic.jpeg" class="d-block w-100" alt="Slide 2">
      </div>
      <div class="carousel-item">
        <img src="/images/couplepic2.jpeg" class="d-block w-100" alt="Slide 3">
      </div>
    </div>

    <!-- Left and right controls -->
    <button class="carousel-control-prev" type="button" data-bs-target="#carousel" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carousel" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
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

/*-----Image Design-----*/
#carousel{
  flex: 1;
  width: 50%;
  overflow: hidden;
  height: 450px;
  padding-left: 40px;
  border-radius: 20px;
}

.carousel-item img {
  width: 50%;
  height: 450px;
  object-fit: cover;
  border-radius: 20px;
}

.error-messages{
  color: red;
  font-size: 0.9rem;
  text-align: center;
}

>>>>>>> origin/Jaden
</style>
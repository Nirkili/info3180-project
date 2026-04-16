<script setup>
//Login user function in here?

</script>



<template>
  
    <div class="container">

        <div class="form-section">

            <h1>Welcome Back!</h1>

            <form @submit.prevent="loginUser">
                <input type="text" required v-model="Username" placeholder="  Username">
                <input type="password" required v-model="Password" placeholder="  Password">
                <button type="submit">Login</button>

                <p>Don't have an account? <router-link :to="{ name: 'register_user' }">Register here!</router-link></p>
            </form>

        </div>

        <div class="image-display">

            <img src="/images/login_image_1.jpg">

        </div>

  </div>

</template>


<style scoped>


h1 {
    padding-bottom: 20px;
}

.container {
  display: flex;
  width: 100%;
}


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
}

input {
    border-radius: 20px;
}

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

a {
  color: #9a60ab;
  text-decoration: none;
  font-weight: bold;
}


</style>
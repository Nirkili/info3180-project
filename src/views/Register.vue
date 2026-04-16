<script setup>
//Register user functionality

</script>



<template>
  
    <div class="container">

            <h1>Ready to find love?</h1>

            <form @submit.prevent="registerUser">
                <div class="labels">

                    <div class="section">
                        <input type="text" required v-model="Username" placeholder="  Username">
                        <input type="text" required v-model="FirstName" placeholder="  FirstName">
                        <input type="text" required v-model="LastName" placeholder="  LastName">
                        <input type="password" required v-model="Password" placeholder="  Password">
                    </div>
                    
                    <div class="section">
                        <input type="text" required v-model="Email" placeholder="  Email">
                        <input type="text" required v-model="Birthdate" placeholder="  mm/dd/yyyy">
                        
                        <select required v-model="Gender">
                            <option disabled value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Non-binary">Non-binary</option>
                        </select>
                       
                        <select required v-model="Preference">
                            <option disabled value="">Select Preference</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Non-binary">Non-binary</option>
                        </select>
                    </div>

                </div>

            <button type="submit">Register</button>

                <p>Already have an account? <router-link :to="{ name: 'login' }">Login</router-link></p>
            </form>

        </div>


</template>


<style scoped>
h1 {
    padding-top: 20px;
}


.container {
    display: flex;
    flex-direction: column;
    /*margin-top: 80px;*/
    margin-bottom: 80px;
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    align-items: center;
    width: 50%;
}


.section {
    display: flex;
    flex-direction: column;
    padding: 40px;
    gap: 15px;
 
}

.labels {
    display: flex;
    flex-direction: row;
    height: 200px;
    padding-bottom: 15px;
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

input, select {
    border-radius: 20px;
    height: 80px;
}

a {
  color: #9a60ab;
  text-decoration: none;
  font-weight: bold;
}
</style>
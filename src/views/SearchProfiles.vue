<template>
    <div id = "searchContainer">
        <form method = "GET" action = "{{url_for('search_course')}}" @submit.prevent="searchUsers">
            <div class="input-group mb-4 search-users">
                <div class="input-group mb-4">
                    <input type="text" class = "form-control" name = "searchTerm" placeholder="Search users...." v-model.trim= "searchTerm">
                    <button type = "submit" id = "search" class="btn btn-outline-secondary"><i class="fa-solid fa-magnifying-glass"></i></button>
                </div>

                <div id = "filtContainer">
                    <select v-model = "filter1" name = "filter1" class=" filtGrp">
                        <option value = "none" disabled selected hidden>Age Range</option>
                        <option value = "18-24">18-24</option>
                        <option value = "25-30">25-30</option>
                        <option value = "30-40">30-41</option>
                        <option value = ">41">>41</option>
                    </select>

                    <select v-model = "filter2" name = "filter2" class="filtGrp">
                        <option value = "none" disabled selected hidden>Gender</option>
                        <option value = "Female">Female</option>
                        <option value = "Male">Male</option>
                        <option value = "Non-binary">Non-Binary</option>
                    </select>

                    <select v-model = "filter3" name = "filter3" class="filtGrp">
                        <option value="none" disabled selected hidden>Location</option>
                        <option value = "Kingston">Kingston</option>
                        <option value = "St. Andrew">St. Andrew</option>
                        <option value = "St. Thomas">St. Thomas</option>
                        <option value = "Portland">Portland</option>
                        <option value = "Trelawny">Trelawny</option>
                        <option value = "Clarendon">Clarendon</option>
                        <option value = "Manchester">Manchester</option>
                        <option value = "St. Elizabeth">St. Elizabeth</option>
                        <option value = "Westmoreland">Westmoreland</option>
                        <option value = "Hanover">Hanover</option>
                        <option value = "St. Mary">St. Mary</option>
                        <option value = "St. Ann">St. Ann</option>
                        <option value = "St. James">St. James</option>
                        
                    </select>
                </div>
            </div>

            <button class = "btn btn-custom submitGrp" type = "button" @click = clearFilt ><i>Clear All Filters</i></button>

        </form>
    </div>
    <div class = "searchRes" v-if ="users.length > 0">
        <div v-for= "user in users" :key = user.user_ID class = "card">
            <div class = "imgContainer">
                <img :src = "user.photo" alt = "profile picture"/>
            </div>
            <div class = "card-title">
                <p>{{ user.f_name }} {{ user.l_name }}, {{ user.age }}</p>
            </div>      
            <div class = "card-body">
                <p class = "card-subtitle text-muted">@{{ user.username }}</p>
                <p>{{ user.gender }}</p>
                <p>{{ user.location }}</p>
            </div>
        </div>
    </div>
    <div v-else id = "noRes">
        <p>No user matches this request.</p>
    </div>

</template>

<script setup>

    import { ref, onMounted } from 'vue';

    const searchTerm = ref("");
    const filter1 = ref("none");
    const filter2 = ref("none");
    const filter3 = ref("none");
    const users = ref([]);

    function searchUsers(){
        const params = new URLSearchParams({
            searchTerm: searchTerm.value,
            filter1: filter1.value,
            filter2: filter2.value,
            filter3: filter3.value
        });
        fetch(`/api/v1/user/search?${params}`,{
            method: 'GET'
        })
        .then(response => response.json())
        .then (function (data) { 
            users.value = data; 
        }) 
        .catch(function (error) { 
            console.log(error); 
        }); 
    }
    
    function clearFilt(){
        searchTerm.value = ""
        filter1.value = "none"
        filter2.value = "none"
        filter3.value = "none"
    }

    onMounted(() => {
        searchUsers();
    });

</script>

<style>
    
    .searchRes{
        display: grid;
        grid-template-columns: repeat(2,1fr);
        gap: 15px;
        max-height: 1000px;
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

    #search{
        background-color: #4a154b;
    }
    #searchContainer{
        padding: 50px;
        display: flex;
        justify-content: center;
        flex-direction: row;
    }
    #filtContainer{
        display: flex;
        flex-direction: row;
        gap: 30px;
        padding-left: 10px;
    }
    .filtGrp{
        border-radius: 5px;
        padding: 10px;
        color: white;
        background-color: #4a154b;
    }

    #noRes{
        display: flex;
        justify-content: center;
        color: grey;
    }

    .submitGrp{
        width: 100%;
        color: white;
        background-color: #4a154b;
    }

    .submitGrp:hover{
        background-color: #E95DA1;
    }
</style>
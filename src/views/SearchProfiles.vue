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
                        <option value = "25-29">25-29</option>
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

                    <select v-model="filter4" name="filter4" class="filtGrp">
                        <option value="none" disabled selected hidden>Interests</option>
                        <option value="Coding">Coding</option>
                        <option value="Investing">Investing</option>
                        <option value="Entrepreneurship">Entrepreneurship</option>
                        <option value="Fitness">Fitness</option>
                        <option value="Meditation">Meditation</option>
                        <option value="Reading">Reading</option>
                        <option value="Learning">Learning</option>
                        <option value="Writing">Writing</option>
                        <option value="Photography">Photography</option>
                        <option value="Tech">Tech</option>
                        <option value="Science">Science</option>
                        <option value="Travel">Travel</option>
                        <option value="Cooking">Cooking</option>
                        <option value="Music">Music</option>
                        <option value="Social Media">Social Media</option>
                    </select>
                </div>
            </div>

            <button class = "btn btn-custom submitGrp" type = "button" @click = clearFilt ><i>Clear All Filters</i></button>

        </form>
    </div>
    <<!--div class="search-res-container">-->
    <div class = "searchRes" v-if ="users.length > 0">
        <div>
            <label for = "sort">Sort By:</label>
            <select v-model = "sort" name = "sort" class="filtGrp">
                <option value = "ASC">Ascending</option>
                <option value = "DESC">Descending</option>
                <option value = "Age">Age</option>
                <option value = "date_created">Date Created</option>
            </select>
        </div>
        <div v-for= "user in users" :key = "user.userID">
            <ProfileCard :user="user">
                <a>Bookmark Icon goes here</a>
            </ProfileCard>

        </div>
    </div>
    <div v-else id = "noRes">
        <p>No user matches this request.</p>
    </div>
<!--</div>-->
    
</template>

<script setup>

    import { ref, onMounted } from 'vue';
    import ProfileCard from '@/components/ProfileCard.vue';

    const searchTerm = ref("");
    const filter1 = ref("none");
    const filter2 = ref("none");
    const filter3 = ref("none");
    const filter4 = ref("none");
    const sort = ref("none");
    const users = ref([]);
    const csrf_token = ref("");


    function searchUsers(){
        const params = new URLSearchParams({
            searchTerm: searchTerm.value,
            filter1: filter1.value,
            filter2: filter2.value,
            filter3: filter3.value,
            filter: filter4.value,
            sort: sort.value
        });
        fetch(`/api/v1/user/search?${params}`,{
            method: 'GET',
            headers:{'X-CSRFToken': csrf_token.value,}
        })
        .then(response => response.json())
        .then (function (data) { 
            users.value = data; 
            console.log(data)
        }) 
        .catch(function (error) { 
            console.log(error); 
        }); 
    }
    
    function clearFilt(){
        searchTerm.value = "";
        filter1.value = "none";
        filter2.value = "none";
        filter3.value = "none";
        filter4.value = "none";
        sort.value = "ASC";
    }

    onMounted(() => {
        searchUsers();
    });

</script>

<style>

    .main-content{
        background-color: none;
    }
    
    .searchRes{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        width: 100%;
        margin: 0 auto;
    }

    @media (min-width: 1024px) {
        .searchRes {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    #search{
        background-color: #4a154b;
    }

    #searchContainer{
        padding: 50px;
        padding-bottom: 20px;
        padding-top: 20px;
        display: flex;
        justify-content: center;
        flex-direction: row;
        border-radius: 20px;
        position: sticky;


        margin-bottom: 20px;
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
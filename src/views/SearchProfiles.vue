<script setup>
    //Import lifecycle hook and ref from Vue and the ProfileCard component.
    import { ref, onMounted } from 'vue';
    import ProfileCard from '../components/ProfileCard.vue';

    const searchTerm = ref("");
    const filter1 = ref("none");
    const filter2 = ref("none");
    const filter3 = ref("none");
    const filter4 = ref("none");
    const sort = ref("none");
    const sort1 = ref("none");
    const users = ref([]);
    const csrf_token = ref("");
    const state = ref(false);
    const message = ref("");

    //Function sends a POST request to the server with the search term, filters and sorts applied by the user. The server then returns a list of users that match the search request which is stored in the users variable.
    function searchUsers(){
        fetch(`/api/v1/search`,{
            method: 'POST',
            headers:{'X-CSRFToken': csrf_token.value,
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                searchTerm: searchTerm.value,
                filter1: filter1.value,
                filter2: filter2.value,
                filter3: filter3.value,
                filter4: filter4.value,
                sort: sort.value,
                sort1: sort1.value
            })
        })
        .then(response => response.json())
        .then (function (data) { 
            users.value = data; 
        }) 
        .catch(function (error) { 
            console.log(error); 
        }); 
    }

    //Function to add a profile to bookmarks. Accepts the profileID of the user to be bookmarked.
    function addbookmark(profile_ID){
        fetch(`/api/v1/bookmarks/${profile_ID}`,{
            method: 'POST',
            headers:{'X-CSRFToken': csrf_token.value,
            'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then (function (data) { 
            console.log(data);
            searchUsers(); 

            if(data.added){
                message.value = data.message;
                state.value = data.added;
                setTimeout(() => state.value = false, 3000)
            }
        })

    }

    //Function to remove a profile from bookmarks. Accepts the profileID of the user to be removed from bookmarks.
    function removebookmark(profile_ID){

        //Confirmation prompt to confirm if the user wants to remove the bookmark. Returns if the user selects cancel.
        if (!window.confirm("Are you sure you want to remove this bookmark?")) {
        return; 
        }

        //If the user confirms, sends a DELETE request to the server to remove the bookmark. After the bookmark is removed, the search results are refreshed.
        fetch(`/api/v1/bookmarks/${profile_ID}`, {
            method: 'DELETE',
            headers:{'X-CSRFToken': csrf_token.value,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then (function (data) { 
            console.log(data);
            searchUsers();

            if(data.removed){
                message.value = data.message;
                state.value = data.removed;
                setTimeout(() => state.value = false, 3000)
            }
        })
    }
    
    //Function to clear all filters and sorts applied and refreshes the search results.
    function clearFilt(){
        searchTerm.value = "";
        filter1.value = "none";
        filter2.value = "none";
        filter3.value = "none";
        filter4.value = "none";
        sort.value = "none";
        sort1.value = "none";

        searchUsers();
    };

    //Function to get the CSRF token from the server which is required to make POST and DELETE requests. The token is stored in the csrf_token variable.
    function getCsrfToken() {
        return fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {

            csrf_token.value = data.csrf_token
        })
        .catch((error) => {
            console.log(error)
        });
    };

    //When the component is mounted, the CSRF token is retrieved and stored first and then searchUsers function is called to display all users.
    onMounted(async () => {
        await getCsrfToken();
        searchUsers();
    });

</script>




<template>
    <div v-if= "state" class="alert alert-successs" role="alert">
        {{message}}
    </div>
    <div id = "searchContainer">
        <!--Search Bar and all filters that can be used to search for a user.-->
        <form method = "GET" action = "{{url_for('search_course')}}" @submit.prevent="searchUsers">
            <!--Search Bar-->
            <div class="input-group mb-4 search-users">
                <div class="input-group mb-4">
                    <input type="text" class = "form-control" name = "searchTerm" placeholder="Search users...." v-model.trim= "searchTerm">
                    <button type = "submit" id = "search" class="btn btn-outline-secondary"><i class="fa-solid fa-magnifying-glass"></i></button>
                </div>
                <!--Filters for age range, interests, gender and location-->
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
            
            <!--Button to clear all filters and sorts applied.-->
            <button class = "btn btn-custom submitGrp" type = "button" @click = clearFilt ><i>Clear All Filters</i></button>

        </form>
    </div>

    <!--Sort Panel for age and date created if any user loads.-->
    <div id = "sortPanel" v-if ="users.length > 0">
        <div id = "sorts">
            <span for = "sort">Sort By:</span>
            <select v-model = "sort" name = "sort" class="sort" @change="searchUsers">
                <option value="none" disabled selected hidden>Age</option>
                <option value = "ASC">Ascending</option>
                <option value = "DSC">Descending</option>
            </select>

            <select v-model = "sort1" name = "sort1" class="sort" @change="searchUsers">
                <option value="none" disabled selected hidden>Date Created</option>
                <option value = "ASC1">Earliest</option>
                <option value = "DSC1">Latest</option>
            </select>
        </div>
    </div>

    <!--Displays the search results if any users are found. If not, displays a message that no users match the search request.-->
    <div class = "searchRes" v-if ="users.length > 0">
        <div v-for= "user in users" :key = user.user_ID>
            <ProfileCard :user = "user">
                <!--Checks if users is bookmarked or not by the current user and provides appropriate action.-->
                <a v-if="user.bookmarked"  @click="removebookmark(user.profile_ID)" class="bookmark"><i class="bi bi-bookmark-fill">Remove Bookmark</i></a>
                <a v-else @click="addbookmark(user.profile_ID)" class="bookmark"><i class="bi bi-bookmark">Add Bookmark</i></a>
            </ProfileCard>
        </div>
    </div>
    <div v-else id = "noRes">
        <p>No user matches this request.</p>
    </div>
<!--</div>-->
    
</template>



<style scoped>

    .main-content{
        background-color: none;
    }
    
    .searchRes{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 30px;
        width: 100%;
        margin: 0 auto;
    }

    @media (min-width: 1024px) {
        .searchRes {
            grid-template-columns: repeat(2, 1fr);
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

    #sortPanel{
        display: flex;
        color: white;
        justify-content: center;
        padding-bottom: 30px;
    }

    #filtContainer, #sorts{
        display: flex;
        flex-direction: row;
        gap: 30px;
        align-items: center;
    }

    .filtGrp{
        border-radius: 5px;
        padding: 10px;
        color: white;
        background-color: #4a154b;
    }

    .sort{
        border-radius: 5px;
        padding: 10px;
        color: #4a154b;
        background-color: white;
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

.alert {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #E95DA1;
    color: white;
    padding: 20px;
    border-radius: 10px;
    z-index: 9999;
}

    .submitGrp:hover{
        background-color: #E95DA1;
    }

    .bookmark{
        color: #E95DA1;
        cursor: pointer;
        text-decoration: none;


    }

    .bookmark:hover{
      color: #4a154b;
    }
</style>
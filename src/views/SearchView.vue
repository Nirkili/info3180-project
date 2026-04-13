<template>
    <div id = "searchContainer">
        <form method = "GET" action = "{{url_for('search_course')}}" @submit.prevent="searchUsers">
            <div class="row g-2 search-users">
                <div class = "col-md-6">
                    <input type="text" class = "c" name = "searchTerm" placeholder="Search users...." v-model.trim= "searchTerm">
                </div>

                <div class = "col-md-2">
                    <select v-model = "filter1" name = "filter1" class="fa-solid fa-filter filtGrp">
                        <option value = "none" disabled selected hidden>Age Range</option>
                        <option value = "18-24">18-24</option>
                        <option value = "25-30">25-30</option>
                        <option value = "30-40">30-40</option>
                        <option value = ">41">>41</option>
                    </select>
                </div> 
                <div class = "col-md-2">
                <select v-model = "filter2" name = "filter2" class="fa-solid fa-filter filtGrp">
                    <option value = "none" disabled selected hidden>Gender</option>
                    <option value = "Female">Female</option>
                    <option value = "Male">Male</option>
                    <option value = "Non-Binary">Non-Binary</option>
                </select>
                </div> 
                <div class = "col-md-2">
                <select v-model = "filter3" name = "filter3" class="fa-solid fa-filter filtGrp">
                    <option value="none" disabled selected hidden>Location</option>
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
                </div> 
            </div>
                
                <div id = "btnGroup">
                    <button type = "submit" ><i class="fa-solid fa-magnifying-glass submitGrp"></i></button>

                    <button class = "submitGrp" type = "button" @click = clearFilt ><i>Clear All Filters</i></button>
                </div>
        </form>
    </div>
    <div class = "searchRes" v-if ="users.length > 0">
        <div v-for= "user in users">
            <img :src = "user.photo"/>
            <p>{{ user.user_name }}</p>
            <p>{{ user.f_Name }} {{ user.l_Name }}</p>
            <span>{{ user.age }}</span>
            <p>{{ user.gender }}</p>
            <p>{{ user.location }}</p>
        </div>
    </div>
    <div v-else>
        <p>No users match request.</p>
    </div>

    
</template>

<script>
    export default{
        data(){
            return{searchTerm: "", filter1: "none", filter2: "none",filter3: "none", users: []};
        },
        methods: {
            searchUsers(){
                const params = new URLSearchParams({
                    searchTerm: this.searchTerm,
                    filter1: this.filter1,
                    filter2: this.filter2,
                    filter3: this.filter3
                });
                fetch(`/api/v1/user/search?${params}`,{
                    method: 'GET'
                })
                .then(function (response) { 
                    return response.json(); 
                }) 
                .then(function (data) { 
                    this.users = data; 
                }) 
                .catch(function (error) { 
                    console.log(error); 
                }); 
            },
            clearFilt(){
                this.searchTerm = ""
                this.filter1 = "none"
                this.filter2 = "none"
                this.filter3 = "none"
                this.searchUsers();
            }
        }
    };
</script>

<style>
    .searchRes{
        display: grid;
        grid-template-columns: 50% 50%;
        height: 450px;
        gap: 15px;
    }

    #searchContianer{
        padding: 50px;
        margin-top: 50px;
        max-height: 75%;
    }
    #btnGroup{
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .submitGrp{
        width: 80%;
        color: white;
    }
</style>
<script setup>
  const first_name = localStorage.getItem("first_name");
  
</script>

<template>
  <aside class="nav-bar">

    <div class="user">
       <img src="/images/profile.jpg" alt="pic">
      <div class="name">Hi {{ first_name }}!</div>
     
    </div>
   

    <div class="links">
      <hr>
      <ul>
        <li>
          <RouterLink to="/home" class=""><i class="fa-solid fa-house"></i>Home</RouterLink>
        </li>
        <li>
          <RouterLink to="/matches" class=""><i class="fa-solid fa-heart"></i>Matches</RouterLink>
        </li>
        <li>
          <RouterLink to="/bookmarks" class=""><i class="fa-solid fa-bookmark"></i>Bookmarks</RouterLink>
        </li>
      </ul>

    </div>
  </aside>
  
  </template>

  <style scoped>
  

  .nav-bar{
    display: flex;
    flex-direction:column;
    width: 220px;
    height: 100%;
    background-color: rgb(255, 255, 255);
    gap:20px;
    border-radius: 20px;
    overflow-y: auto;
    box-shadow: 0 0 10px rgba(95, 10, 164, 0.1);
  }

  img{
    border-radius: 100px;
    height: 100px;
  }

  .name{
    font-size: 1.5rem;
    color:  rgb(85, 13, 103);
    font-weight: 600px;
  }

  .user{
    display:flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding-top: 40px;
    gap: 20px;
    margin-bottom: 20px;
    }

    .links i{
      margin-right: 8px;
      color:  rgb(85, 13, 103);
    }

    .links ul {
      list-style: none;
      padding: 0;
      margin: 0;
    }

    .links li{
      margin-bottom: 35px;
      position: relative;
    }

    .links li a{
      display: flex;
      align-items: center;
      width: 100%;
      padding: 12px;
      border-radius: 12px;
      text-decoration: none;
      justify-content: center;
      color: black;
      transition: all 0.25s ease;

    }

    .links li a:hover{
      background-color:  rgb(238, 219, 243); 
      padding: 15px;
      cursor: pointer;
    }

    .links li a:hover::before {
      content: "";
      position: absolute;
      left: 0;
      top: 8px;
      bottom: 8px;
      width: 4px;
      background-color:  rgb(85, 13, 103); 
      border-radius: 4px;
      transition: all 0.25s ease;
    }

    .links a{
      text-decoration: none;
      border-radius: 20px;
      color: black;


    }

    hr{
      color:  rgb(85, 13, 103);
    }

  

</style>
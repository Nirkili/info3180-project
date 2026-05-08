<template>
  <div class="about-container">
    <div id = "heading">
      <h1>About Us</h1>
    </div>

    <hr>
    <h2><i>Who Are We?</i></h2>
    <hr>

    <section class = "sections">
      <h3>Our Story</h3>

      <p>Created straight from the homes from talented university students, we present to you DriftDater. DriftDater is a monumental dating app created to revolutionize the dating space in Jamaica. We are a team of passionate individuals who are dedicated to creating a safe and enjoyable dating experience for our users. We believe that everyone deserves to find love and companionship, and we are committed to providing a platform that makes it easy for people to connect with each other.</p>  
      
      <h3>Our Team</h3>
      <p>Our team is composed of individuals with diverse backgrounds and skills, all united by a common goal: to create a better dating experience for everyone. Here at DriftDater, we proudly represent a diverse group of professionals dedicated to making a difference in the world of dating. As such, we have an all-female development team.

    </p>
      
    <div id="team">
      <div class = "team-member">
        <img class= "team-img" src="/images/tara.jpeg" alt="Tara-Lee Donald">
        <p>Tara-Lee Donald</p>
        <p><i>Lead Q/A & Testing</i></p>
      </div>

      <div class = "team-member">
        <img class = "team-img" src="/images/jaden.jpeg" alt="Jaden Anthony">
        <p>Jaden Anthony</p>
        <p><i>Lead Frontend Developer</i></p>
      </div>

      <div class = "team-member">
        <img class = "team-img" src="/images/dana.jpeg" alt="Dana Archer">
        <p>Dana Archer</p>
        <p><i>Project Manager<br>Lead Backend Developer</i></p>
      </div>

    </div>

    <h3>Our Values</h3>
    <p>
      We are committed to creating a safe and enjoyable dating experience for our users. Our core values include:
    </p>

    <ul>
      <li><strong>Integrity:</strong> We believe in being honest and transparent in all our interactions.</li>
      <li><strong>Respect:</strong> We treat all users with respect and dignity.</li>
      <li><strong>Innovation:</strong> We continuously strive to improve our platform and user experience.</li>
    </ul>
  </section>

  <hr>
  <h2><i>Why Choose DriftDater?</i></h2>
  <hr>
  <div>
    <section class = "sections">
      <p>
        At DriftDater, we offer a wide range of features to help our users find their perfect match. Our app is designed to be user-friendly and intuitive, making it easy for anyone to use. We offer a variety of features such as: 
      </p>
      <ul>
        <li>Profile Creation</li>
        <p>
          Allows a user to create a detailed profile with information about themselves including their interests and preferences.
        </p>
        <li>Profile Search</li>
        <p>
          Enables users to search for potential matches based on various criteria such as age, location, and interests. This information can then be sorted by age and date of account creation.
        </p>
        <li>Messaging System</li>
        <p>
          Provides a safe and secure environment for users to communicate with users whom they have matched with.
        </p>
        <li>Matchmaking Algorithm</li>
        <p>
          Utilizes a sophisticated algorithm to suggest potential matches based on user preferences and behavior on the app and calculates a score to determine compatibility.
        </p>
        <li>Bookmarking System</li>
        <p>
          Allows users to save profiles they are interested in for easy access later.
        </p>

        <li>Quiet Browsing</li>
        <p>
          Allows users to browse profiles while being invisible to other users by allowing private visibility.
        </p>
      </ul>
    </section>
    </div>
  </div>
</template>

<style>
.about-container{
    padding: 40px;
    color: white;
}

#heading{
    display: flex;
    justify-content: center;
    padding-bottom: 30px;
}

.sections{
    display: flex;
    justify-content: space-between;
    gap: 40px;
    margin-bottom: 60px;
    flex-wrap: wrap;
    flex-direction: column;
}

.sections p{
    flex: 1;
    min-width: 300px;
}

h2{
    font-size: 30px;
    margin-bottom: 15px;
}

h3{
    font-size: 24px;
    margin-bottom: 10px;
}

.sections p{
    line-height: 1.8;
    font-size: 1.1rem;
}

#about-img{
    width: 200px;
    border-radius: 20px;
    object-fit: cover;
    float: right;
}

#team{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    flex-wrap: wrap;
    flex-direction:row;
}
.team-member{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    justify-content: center;
    text-align: center;
}

.team-member i{
    font-size: 14px;
    color: rgb(215, 211, 211);}

#team p{
    margin: 0;
}

.team-img{
    width: 150px;
    border-radius: 100px;
    object-fit: cover;
}
</style>
 
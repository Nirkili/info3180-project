# INFO3180 FINAL PROJECT DOCUMENTATION

## PROJECT DESCRIPTION:

DriftDater is a dating app that allows registered users to create detailed profiles, discover compatible users based off similarity calculations and initiate connections with other users. Users will be able to:

 - Create their own dating profile
 - Edit their own dating profile
 - Search for other users and manage data using sorts and filters (provided that other user's visibility status' are set to public) 
 - Like other users' profiles
 - Dislike other users' profiles 
 - Bookmark other users' profiles
 - Remove user profiles from their bookmarks
 - Chat with users that were matched with within the system. (A match occurs when both users liked each other's profile)

## TEAM MEMBERS AND ROLES:

Dana Archer - Backend Lead, Project Manager
Jaden Anthony - Frontend Lead
Tara-Lee Donald - QA/Testing Lead 

## SETUP INSTRUCTIONS: 

1. Clone the starter repository 
2. Create a Python virtual environment: python -m venv venv 
3. Activate: source venv/bin/activate (Linux/Mac) or .\venv\Scripts\activate 
(Windows) 
4. Install dependencies: pip install -r requirements.txt 
5. Create database: flask db init, flask db migrate, flask db upgrade 
6. Start backend: flask --app app --debug run (default: http://localhost:5000) 
7. In new terminal, start frontend: npm install && npm run dev (default: 
http://localhost:5173)
8. Run generator file to generate fake users for the app if needed.

## API DOCUMENTATION:


1. ROUTE - `/api/v1/auth/register`

register() - The register endpoint accepts no parameters and creates a user using the `POST` method. If the username is not available to choose from, The message "Username not available" for the field Username is returned, along with status code 400. If the email is already registered, the message "Email already registered" is returned for the field Email along with status code 400. If successful, returns a status code of 201, the newly created user ID and a message saying "Registration successful". If not, a response code of 400 is returned and all error messages relating to the form are returned.

2. ROUTE - `/api/v1/auth/login`

login() - The login endpoint accepts no parameters and authorizes a user to use the app using the `POST` method. If successful, the enpoint returns a status code of 200, the user's ID, first name and last name and a message saying "Login successful". If their password cannot be verified, a status code of 401 is returned and a message "Invalid email or password" for the field credentials. If the form cannot be validated, all error messages relating to the form are returned along with status code 400 is returned.

3. ROUTE - `/api/v1/auth/logout`

logout() - This endpoint accepts no parameters. It uses the `POST` method and returns status code 200 and a message "Logged out successfully" when the user logs out.

4. ROUTE - `/api/v1/auth/status`

auth_status() - This endpoint accepts no parameters. It uses the `GET` method and checks if the user is authenticated and if so, returns the 'logged in' status as True and the current user ID, along with status code 200. If not, returns the 'logged in' status as False, along with status code 200.

5. ROUTE - `/api/v1/profile`

get_my_profile() - This endpoint accepts no parameters. It uses the `GET` method and gets the current user's profile. If found, return all information about the user's profile such as the profileID, userID, gender, location, visibility status of their profile, picture, gender preference, whether they want children, Type of relationship desired and age. The status code 200 is also returned. If the profile for the current user cannot be found, an error message "Profile not found" is returned along with status code 404.

6. ROUTE - `/api/v1/profile`

update_profile() – This endpoint accepts no parameters. It uses the `PUT` method and updates the current user’s profile information using data from a submitted form. If the form is successfully validated and the profile exists, a message "Profile update successful" is returned with status code 200. If the profile does not exist, a 404 error with the message "Profile not found" is returned. If the form fails validation, all error messages related to the form are returned with status code 400.


7. ROUTE - `/api/v1/profile/me`

get_my_profile() – Uses the `GET` method and accepts no parameters. The purpose of this function is to retun the profile of the current user. If the profile exists, all profile details are returned along with status code 200. If no profile is found, an error message "Profile not found" is returned with status code 404.

8. ROUTE - `/api/v1/profile/<int:profile_id>`

get_profile(profile_id) – Uses the `GET` method and accepts a profile ID as a parameter. If the profile exists, all profile details are returned along with status code 200. If no profile is found, an error message "Profile not found" is returned with status code 404.

9. ROUTE - `/api/v1/user/search`

searchUsers() – Uses the `GET` method and allows users to search for other public users based on a search term and optional filters such as age range, gender, location, and interests. This information can also be managed through sorts by a user's age and date of account creation. Upon searching, a list of matching users with their account details like a user's profileID, username, name, gender, age, location, bio and photo is returned along with status code 200.

10. ROUTE - `/api/v1/user/bookmarks`

getBookmarkedUsers() – Uses the `GET` method and retrieves all profiles bookmarked by the currently logged-in user. A list of bookmarked users with information such as the user's profileID, username, name, gender, age, location, bio and photo is returned along with status code 200.

11. ROUTE - `/api/v1/user/bookmarks/<int:profile_ID>`

deleteBookmarkedUser(profile_ID) – Uses the `DELETE` and accepts the the profile ID of the user to be deleted as a parameter. If successful, a message "Bookmark deleted successfully" is returned with status code 200 and removed is set to True. If the bookmark does not exist, an appropriate error message is returned with status code 404 and removed is set to false.

12. ROUTE - `/api/v1/user/bookmarks/<int:profile_ID>`

addBookmarkedUser(profile_ID) – Uses the `POST` method and accepts the profile ID of the user to be bookmarked as a parameter. If the bookmark is successfully created, a message "Bookmark added successfully" is sent and returned with status code 201 and added is set to True. If the profile is already bookmarked, a message "Bookmark already exists" is returned with status code 400 and added is set to False.

13. ROUTE - `/api/v1/home`

matching_algorithm() – This endpoint accepts no parameters. It uses the `GET` method and generates a list of potential matches for the current user based on their profile and interests. It returns a list of user and profile details for each user, compatibility score and percentage in descending order of score and returned with status code 200.


14. ROUTE - `/api/v1/profile/interest`

set_interests() – Uses the `POST` method and allows the current user to set their interests. The selected interests are stored in the database. Upon successful completion, a confirmation message "Interests saved." is returned with status code 200.

15. ROUTE - `/api/v1/csrf-token`

get_csrf() – Uses the `GET` method and generates and returns a CSRF token required for secure form submissions. The token is returned along with status code 200 if generated successfully.

16. ROUTE - `/api/v1/images/<filename>`

uploads(filename) – Uses the `GET` method and accepts a filename to be retrieved as a parameter. The requested image is returned if it exists along with status code 200 if it can be found.


17. ROUTE - `/api/v1/home/<int:user_ID>`

rate_user(user_ID) - Accepts user to be liked as a parameter. If that user is not found, returns an error message 'Profile not found.' and status code 404. If the user was already interacted with, a message "You have already interacted with this user" is shown with error code 400. If the current user passed the user associated with the ID in the parameter, the message "Action recorded" is sent, matched is returned as False and returned along with status code 201. If the like was not mutual, the message "Action recorded" is sent, matched is returned as False and returned along with status code 201. If there was a mutual like, the message "You have a match!" is sent, matched is set to True and is returned along with status code 201.

18. ROUTE - `/api/v1/matches`

get_matches() - This endpoint accepts no parameters. Get matches for current users. Returns user and profile information such as userID, username, name, age, bio, location and  profile picture along with status code 200. If no matches can be found, the message "No Matches" is returned along with status code 404.

19. ROUTE - `/api/v1/chats/<int:chat_ID>`

get_chat_history(chat_ID) - Accepts chatID of chat to get messages for. Function returns the message list along with status code 200.

20. ROUTE - `/api/v1/chats`

get_chats() - This endpoint accepts no parameters. Gets all chats for the current user and returns the chat list along with status code 200.

21. ROUTE - `/api/v1/interests`

get_interests() - This endpoint accepts no parameters. Gets all interests for the user to select from during registration. 

--------------------------------------
### Helper Functions
--------------------------------------
send_message(data)- Saves message to database using socket programming.

join(data) - Enables a user to connect to a chat using socket programming.

unauthorized() - Sends an unauthorized message and status code 401.

form_errors(form) - Accepts the form it would retrive errors for as a parameter. Returns all error messages associated with the form.

add_header(response) - Add headers to both force latest IE rendering engine or Chrome Frame, and also tell the browser not to cache the rendered page. 

page_not_found(error) - Takes an error and renders the 404 template if the page cannot be found.

## Limitations

Accuracy of Matching Algorithm - The algorithm is only as accurate as the data provided by the user. It does not facilitate deep learning but an analysis of information entered by the user at the time. Due to this, the matching algorithm may not be able to capture all profiles the user is actually interested in.

Responsiveness of App to Different Screens - Due to the time constraint, the performance of the app with regards to mobbile or television view is unknown and is known to work with standard laptop screens.

Offline Access - DriftDater has been built as an online web application and so features are not guaranteed to work with the absence of a network connection.

Matching System - Once a user matches with another user, they cannot be unmatched. Furthermore, once a chat is started, it cannot be deleted.

Edit Profile - Edit profile currently has not been implemented.



# INFO3180 VueJS and Flask Starter

This template should help get you started developing with Vue 3 on the frontend and Flask as an API on the backend.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## Start Flask API

PROJECT DESCRIPTION:

DriftDater is a dating app that allows registered users to create detailed profiles, discover 
compatible matches, and initiate connections with other users. Users will be able to:

 - Create their own dating profile
 - Edit their own dating profile
 - Search for other users and manage data using sorts and filters (provided that other user's visibility status' are set to public) 
 - Like other users' profiles
 - Dislike other users' profiles
 - Pass other users' profiles 
 - Bookmark other users' profiles
 - Chat with users that were matched with within the system. (A match occurs when both users liked each other's profile)

TEAM MEMBERS AND ROLES:

Dana Archer - 
Jaden Anthony -
Tara-Lee Donald -

SETUP INSTRUCTIONS: 

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

API DOCUMENTATION:

1. ROUTE - `/api/v1/auth/register`
register() - The register endpoint accepts no parameters and creates a user using the `POST` method. If successful, returns a status code of 201, the newly created user ID and a message saying "Registration successful". If not, a response code of 400 is returned and all error messages relating to the form are returned.

2. ROUTE - `/api/v1/auth/login`
login() - The login endpoint accepts no parameters and authorizes a user to use the app using the `POST` method. If successful, the enpoint returns a status code of 200, the user's ID, first name and last name and a message saying "Login successful". If their password cannot be verified, a response code of 401 is returned and a message "Invalid email or password" for the field credentials. If the form cannot be validated, all error messages relating to the form are returned along with status code 400 is returned.




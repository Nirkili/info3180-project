import { io } from 'socket.io-client'

const socket = io('http://localhost:8080', { // Create socket connection to flask server
  withCredentials: true,
  autoConnect: false

})

export default socket // Allows any view component to use it
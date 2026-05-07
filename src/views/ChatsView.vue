<<<<<<< HEAD
<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import socket from '@/socket.js';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore()

let chats = ref([]);
let messages = ref([])
let newMessage = ref('')
let activeChat = ref(null)



async function getChats(){
  return fetch('/api/v1/chats', {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    }
  })

  .then(response => response.json())

  .then(function(data){
    console.log(data)
    chats.value = data.chats;


     const chatID = route.query.chat_ID
      if(chatID){
        const chat = chats.value.find(c => c.chat_ID == chatID)
        if(chat) openChat(chat)
      }
  })

 

  .catch(function(error){
    console.log(error);
  })
}

function getInitials(user_name){
  if(!user_name){
    return '?'
  }
  return  user_name.split(' ').map(word => word[0].toUpperCase()).join('')

}

function openChat(chat){
  activeChat.value = chat;
  getMessages(chat.chat_ID);

  socket.connect();
  socket.emit('join', {room: `room_${chat.chat_ID}`})
}

async function getMessages(chatID){
  fetch(`/api/v1/chats/${chatID}`, {
    method: 'GET',
    headers: {
      'ContentType': 'application/json'
    }
  })

  .then(response => response.json())

  .then(function(data){
    messages.value = data.messages;
  })

  .catch(function(error){
    console.log(error);
  })
}

function sendMessage(){
  if(!newMessage.value) return

  const payload = {
    chat_ID: activeChat.value.chat_ID,
    sender_ID: authStore.userId,
    content: newMessage.value.trim(),
    room: `room_${activeChat.value.chat_ID}`
  }

  console.log('Sending:', payload)  // check this in the browser console
  socket.emit('send_message', payload)

  newMessage.value = '';
  // Add 
}


onMounted(async () => {
      await getChats();


      // Listen for a new message
      socket.on(`receive_message`, (data) => {
        
        if(activeChat.value && data.room === `room_${activeChat.value.chat_ID}`){
            messages.value.push({
            id: Date.now(),
            sender_ID: data.sender_ID,
            content: data.content,
            timestamp: data.timestamp
        })

            const chat = chats.value.find(c => c.chat_ID === activeChat.value.chat_ID)
            if (chat) {
                chat.last_msg = data.content
              }

        
        }
        
      })
    });


  onUnmounted(() => {
    socket.disconnect()
  })










</script>


<template>
  <div class="chat-container">



    <!--Chat List-->
    <div class="chat-list">

      <div class="header">
        My Chats
      </div>

       <div
        v-for="chat in chats"
        :key="chat.chat_ID"
        class="conv-item"
        :class="{ active: activeChat?.chat_ID === chat.chat_ID }"
        @click="openChat(chat)"
      >

        <div class="avatar">{{ getInitials(chat.matched_user_name) }}</div>
        <div class="information">
          <div class="name">{{ chat.matched_user_name }}</div>
          <div class="preview">{{ chat.last_msg }}</div>
        </div>

      </div>
    </div>

    <!--Message Window-->
    <div class="selected"  v-if="activeChat">
      <div class="selected-header">

        <div class="avatar">{{ getInitials(activeChat.matched_user_name) }}</div>
        <div class="name">{{ activeChat.matched_user_name }}</div>


      </div>

      <div class="messages" ref="messagesContainer">
        <div v-for="m in messages" :key="m_ID" class="msg" :class="m.sender_ID === authStore.userId ? 'sent': 'received'">

          {{ m.content }}
          <div class="msg-time">
            {{  m.timestamp }}
          </div>
        </div>
      </div>

      <div class="user-input">
        <input v-model="newMessage" type="text" placeholder="Type your message!"
        @keyup.enter="sendMessage"/>

        <button class="send-btn" @click="sendMessage">Send</button>
      </div>

    </div>

    <!--No chats-->
      <div class="no-chat" v-else>
        Select a chat!

      </div>


  </div>
</template>


<style scoped>

.main-content{
  padding: 0;
}

.chat-container{
   background-color: white;
  display:flex;
  border: 0.5px solid #e0e0e0;
  border-radius: 20px;
  overflow:hidden;
  padding: 15px;
  height: 82vh;

}


.chat-list{
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow-y: auto;
  width: 250px;
  border-right: 1px solid #e0e0e0;

}

.header {
  padding: 16px;
  font-size: 25px;
  font-weight: 500;
  border-bottom: 0.5px solid #e0e0e0;
}


.conv-item{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  cursor: pointer;
  border-bottom: 2px solid purple;
}

.conv-item:active{
 background-color:#9d73ac;
}

.conv-item:hover:not(.active) {
  background: #f5f5f5;
}

.information{
  flex: 1;
  min-width: 0;
}

.name{
  font-size: 15px;
  font-weight: 500;
}

.preview{
  font-size: 12px;
  color: #888;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 2px;
}

.avatar{
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  color: white;
  background-color: #9d73ac;
  border-radius: 20px;
  width: 40px;
  height: 40px;
  
}

.selected{
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.selected-header{
  padding: 14px 16px;
  border-bottom: 0.5px solid #e0e0e0;
  display: flex;
  align-items: center;
  gap: 10px;

}

.no-chat{
  flex: 1;
  display: flex;
  font-size: 1.1em;
  flex-direction: column;
  align-items: center;
  justify-content:center;
  padding: 20px;
  color: #888;
}


/* --- Messages --- */
.messages {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
}

.msg {
  max-width: 65%;
  padding: 8px 12px;
  border-radius: 16px;
  font-size: 13px;
  line-height: 1.5;
}

.msg.received {
  background: #f0f0f0;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

.msg.sent {
  background: #7F77DD;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.msg-time {
  font-size: 10px;
  margin-top: 3px;
  opacity: 0.7;
}

.msg.sent .msg-time {
  text-align: right;
}

/* --- Input --- */
.user-input {
  padding: 12px 16px;
  border-top: 0.5px solid #e0e0e0;
  display: flex;
  gap: 8px;
  align-items: center;
}

.user-input input {
  flex: 1;
  padding: 8px 12px;
  border-radius: 20px;
  border: 0.5px solid #ccc;
  font-size: 13px;
  outline: none;
}

.send-btn {
  background: #7F77DD;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
}

.send-btn:hover {
  background: #6a62c4;
}


=======
<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import socket from '@/socket.js';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore()

let chats = ref([]);
let messages = ref([])
let newMessage = ref('')
let activeChat = ref(null)



async function getChats(){
  return fetch('/api/v1/chats', {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    }
  })

  .then(response => response.json())

  .then(function(data){
    console.log(data)
    chats.value = data.chats;


     const chatID = route.query.chat_ID
      if(chatID){
        const chat = chats.value.find(c => c.chat_ID == chatID)
        if(chat) openChat(chat)
      }
  })

 

  .catch(function(error){
    console.log(error);
  })
}

function getInitials(user_name){
  if(!user_name){
    return '?'
  }
  return  user_name.split(' ').map(word => word[0].toUpperCase()).join('')

}

function openChat(chat){
  activeChat.value = chat;
  getMessages(chat.chat_ID);

  socket.connect();
  socket.emit('join', {room: `room_${chat.chat_ID}`})
}

async function getMessages(chatID){
  fetch(`/api/v1/chats/${chatID}`, {
    method: 'GET',
    headers: {
      'ContentType': 'application/json'
    }
  })

  .then(response => response.json())

  .then(function(data){
    messages.value = data.messages;
  })

  .catch(function(error){
    console.log(error);
  })
}

function sendMessage(){
  if(!newMessage.value) return

  const payload = {
    chat_ID: activeChat.value.chat_ID,
    sender_ID: authStore.userId,
    content: newMessage.value.trim(),
    room: `room_${activeChat.value.chat_ID}`
  }

  console.log('Sending:', payload)  // check this in the browser console
  socket.emit('send_message', payload)

  newMessage.value = '';
  // Add 
}


onMounted(async () => {
      await getChats();


      // Listen for a new message
      socket.on(`receive_message`, (data) => {
        
        if(activeChat.value && data.room === `room_${activeChat.value.chat_ID}`){
            messages.value.push({
            id: Date.now(),
            sender_ID: data.sender_ID,
            content: data.content,
            timestamp: data.timestamp
        })

            const chat = chats.value.find(c => c.chat_ID === activeChat.value.chat_ID)
            if (chat) {
                chat.last_msg = data.content
              }

        
        }
        
      })
    });


  onUnmounted(() => {
    socket.disconnect()
  })










</script>


<template>
  <div class="chat-container">



    <!--Chat List-->
    <div class="chat-list">

      <div class="header">
        My Chats
      </div>

       <div
        v-for="chat in chats"
        :key="chat.chat_ID"
        class="conv-item"
        :class="{ active: activeChat?.chat_ID === chat.chat_ID }"
        @click="openChat(chat)"
      >

        <div class="avatar">{{ getInitials(chat.matched_user_name) }}</div>
        <div class="information">
          <div class="name">{{ chat.matched_user_name }}</div>
          <div class="preview">{{ chat.last_msg }}</div>
        </div>

      </div>
    </div>

    <!--Message Window-->
    <div class="selected"  v-if="activeChat">
      <div class="selected-header">

        <div class="avatar">{{ getInitials(activeChat.matched_user_name) }}</div>
        <div class="name">{{ activeChat.matched_user_name }}</div>


      </div>

      <div class="messages" ref="messagesContainer">
        <div v-for="m in messages" :key="m_ID" class="msg" :class="m.sender_ID === authStore.userId ? 'sent': 'received'">

          {{ m.content }}
          <div class="msg-time">
            {{  m.timestamp }}
          </div>
        </div>
      </div>

      <div class="user-input">
        <input v-model="newMessage" type="text" placeholder="Type your message!"
        @keyup.enter="sendMessage"/>

        <button class="send-btn" @click="sendMessage">Send</button>
      </div>

    </div>

    <!--No chats-->
      <div class="no-chat" v-else>
        Select a chat!

      </div>


  </div>
</template>


<style scoped>

.main-content{
  padding: 0;
}

.chat-container{
   background-color: white;
  display:flex;
  border: 0.5px solid #e0e0e0;
  border-radius: 20px;
  overflow:hidden;
  padding: 15px;
  height: 82vh;

}


.chat-list{
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow-y: auto;
  width: 250px;
  border-right: 1px solid #e0e0e0;

}

.header {
  padding: 16px;
  font-size: 25px;
  font-weight: 500;
  border-bottom: 0.5px solid #e0e0e0;
}


.conv-item{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  cursor: pointer;
  border-bottom: 2px solid purple;
}

.conv-item:active{
 background-color:#9d73ac;
}

.conv-item:hover:not(.active) {
  background: #f5f5f5;
}

.information{
  flex: 1;
  min-width: 0;
}

.name{
  font-size: 15px;
  font-weight: 500;
}

.preview{
  font-size: 12px;
  color: #888;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 2px;
}

.avatar{
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  color: white;
  background-color: #9d73ac;
  border-radius: 20px;
  width: 40px;
  height: 40px;
  
}

.selected{
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.selected-header{
  padding: 14px 16px;
  border-bottom: 0.5px solid #e0e0e0;
  display: flex;
  align-items: center;
  gap: 10px;

}

.no-chat{
  flex: 1;
  display: flex;
  font-size: 1.1em;
  flex-direction: column;
  align-items: center;
  justify-content:center;
  padding: 20px;
  color: #888;
}


/* --- Messages --- */
.messages {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
}

.msg {
  max-width: 65%;
  padding: 8px 12px;
  border-radius: 16px;
  font-size: 13px;
  line-height: 1.5;
}

.msg.received {
  background: #f0f0f0;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

.msg.sent {
  background: #7F77DD;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.msg-time {
  font-size: 10px;
  margin-top: 3px;
  opacity: 0.7;
}

.msg.sent .msg-time {
  text-align: right;
}

/* --- Input --- */
.user-input {
  padding: 12px 16px;
  border-top: 0.5px solid #e0e0e0;
  display: flex;
  gap: 8px;
  align-items: center;
}

.user-input input {
  flex: 1;
  padding: 8px 12px;
  border-radius: 20px;
  border: 0.5px solid #ccc;
  font-size: 13px;
  outline: none;
}

.send-btn {
  background: #7F77DD;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
}

.send-btn:hover {
  background: #6a62c4;
}


>>>>>>> origin/Jaden
</style>
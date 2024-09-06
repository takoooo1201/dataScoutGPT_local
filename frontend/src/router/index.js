// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
//import Chatbot from '../components/chatbotComponent.vue'; // 確保 Chatbot.vue 是你聊天機器人的組件
import ChatbotComponent from '../components/chatbotComponent.vue';

import UploadComponent from '../components/uploadComponent.vue';

const routes = [
  {
    path: '/chatbot',
    name: 'Chatbot',
    component: ChatbotComponent,
  },
  {
    path: '/upload',
    name: 'upload',
    component: UploadComponent,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

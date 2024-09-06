<!-- src/components/ChatBotView.vue -->
<template>
  <div class="chat-container">
    <h1 class="chat-header">Chatbot</h1>
    <div class="chat-window">
      <div
        v-for="(message, index) in chatHistory"
        :key="index"
        :class="['message', message.role === 'user' ? 'user-message' : 'bot-message']"
      >
        <p>{{ message.content }}</p>
      </div>
    </div>
    <div class="input-container">
      <input
        type="text"
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="Type your message..."
        class="chat-input"
      />
      <button @click="sendMessage" class="send-button">Send</button>
    </div>
    <div class="upload-container">
      <input type="file" @change="handleFileUpload" />
      <button @click="uploadFile" class="upload-button">Upload File</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatBotView',
  data() {
    return {
      userInput: '',
      chatHistory: [],
      selectedFile: null,
    };
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === '') return;

      this.chatHistory.push({ role: 'user', content: this.userInput });

      try {
        const response = await axios.post('http://127.0.0.1:5000/chat', {
          prompt: this.userInput,
        });

        this.chatHistory.push({ role: 'bot', content: response.data.response });
      } catch (error) {
        console.error('Error fetching response:', error);
        this.chatHistory.push({ role: 'bot', content: 'Error: Unable to fetch response.' });
      }

      this.userInput = '';
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert('Please select a file to upload.');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        const response = await axios.post('http://127.0.0.1:5000/upload', formData);
        console.log('Upload Response:', response.data);
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    },
  },
};
</script>

<style>
.chat-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #1e1e1e;
  color: #ffffff;
  padding: 20px;
}

.chat-header {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #ffffff;
}

.chat-window {
  width: 100%;
  max-width: 600px;
  height: 400px;
  border: 1px solid #333;
  border-radius: 8px;
  background-color: #2e2e2e;
  padding: 15px;
  overflow-y: scroll;
  margin-bottom: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 8px;
  max-width: 80%;
  word-wrap: break-word;
}

.user-message {
  align-self: flex-end;
  background-color: #4a90e2;
  color: #ffffff;
}

.bot-message {
  align-self: flex-start;
  background-color: #3b3b3b;
  color: #ffffff;
}

.input-container {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 600px;
}

.chat-input {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #444;
  background-color: #2e2e2e;
  color: #ffffff;
  margin-right: 10px;
}

.chat-input::placeholder {
  color: #888;
}

.send-button {
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  background-color: #4a90e2;
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-button:hover {
  background-color: #357ab7;
}

/* 保留之前的樣式並增加檔案上傳按鈕的樣式 */
.upload-container {
  margin-top: 20px;
  display: flex;
  align-items: center;
}

.upload-button {
  margin-left: 10px;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  background-color: #4a90e2;
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.upload-button:hover {
  background-color: #357ab7;
}
</style>

<!-- FileUpload.vue -->
<template>
    <div>
      <input type="file" @change="handleFileUpload" />
      <button @click="uploadFile">Upload</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        selectedFile: null
      };
    },
    methods: {
      handleFileUpload(event) {
        this.selectedFile = event.target.files[0];
      },
      uploadFile() {
        const formData = new FormData();
        formData.append('file', this.selectedFile);
  
        axios.post('http://localhost:5000/uploads', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          console.log('File uploaded successfully', response.data);
        })
        .catch(error => {
          console.error('Error uploading file', error);
        });
      }
    }
  };
  </script>
  
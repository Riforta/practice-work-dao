import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000/api';

const http = axios.create({
  baseURL: BASE_URL,
});

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default http;

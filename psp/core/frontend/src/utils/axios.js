import axios from 'axios';
import router from "@/router";

const ax = axios.create({
  baseURL: `${import.meta.env.VITE_SERVER_URL}`,
  headers: {
    'Content-type': 'application/json'
  },
  withCredentials: true,
});

export { ax };

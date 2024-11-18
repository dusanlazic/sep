import axios from 'axios';
import router from "@/router";

const ax = axios.create({
  baseURL: `${import.meta.env.VITE_SERVER_URL}`,
  headers: {
    'Content-type': 'application/json'
  },
  withCredentials: true,
});

ax.interceptors.response.use(
  (response) => {
    return response;
  },
  (err) => {
    // return other errors
    if (err.response?.status !== 401) {
      return new Promise((_, reject) => {
        reject(err);
      });
    }

    // error on login
    if (err.response?.config?.url === '/auth/login' || window.location.pathname === '/login') {
      return new Promise((_, reject) => {
        reject(err);
      });
    } else if (err.response?.config?.url === '/auth/me') {
      router.push('/login');
      return new Promise((_, reject) => {
        reject(err);
      });
    } else {
      return new Promise((_, reject) => {
        reject(err);
      });
    }
  }
)

export { ax };

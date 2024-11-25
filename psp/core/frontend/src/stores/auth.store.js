import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ax } from '@/utils/axios';

export const useAuthStore = defineStore('auth', () => {
  const session = ref(JSON.parse(localStorage.getItem('session')));
  
  async function fetchSession() {
    try {
      const response = await ax.get(
        '/merchants/me',
      );
      const user = response.data;
      
      session.value = {
        username: user.username,
        title: user.title,
        apiKey: user.api_key
      };

      localStorage.setItem('session', JSON.stringify(session.value));
      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  async function login(username, password) {
    try {
      const response = await ax.post('/merchants/login', {
        username,
        password,
      });
  
      if (!response?.data) {
        return false;
      }
  
      await fetchSession();
  
      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  async function register(data) {
    try {
      const response = await ax.post('/merchants/register', data);
  
      if (!response?.data) {
        return false;
      }
  
      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  async function logout() {
    await ax.post(
      '/merchants/logout',
    );
    clearSession();
  }

  function clearSession() {
    session.value = null;
    localStorage.removeItem('session');
  };

  function isUserLoggedIn() {
    return !!session.value || !!localStorage.getItem('session');
  };

  return { session, fetchSession, clearSession, login, logout, isUserLoggedIn, register };
});

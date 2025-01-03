import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ax } from '@/utils/axios';

export const useAuthStore = defineStore('auth', () => {
  const session = ref(JSON.parse(localStorage.getItem('session')));
  
  async function fetchSession() {
    try {
      const response = await ax.get(
        '/auth/me',
      );
      const user = response.data;
      
      session.value = {
        username: user.username,
        fullName: user.full_name,
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
      const response = await ax.post('/auth/login', {
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
      const response = await ax.post('/auth/register', data);
  
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
      '/auth/logout',
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

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.store';

const router = useRouter();
const authStore = useAuthStore();

const username = ref('');
const password = ref('');
const usernameErrorMessage = ref('');
const passwordErrorMessage = ref('');
const showErrorMessage = ref(false);

const isInputValid = () => {
  const isUsernameValid = username.value.trim().length > 0;
  usernameErrorMessage.value = !isUsernameValid ? 'Username invalid' : '';
  const isPasswordValid = password.value.trim().length > 0;
  passwordErrorMessage.value = !isPasswordValid ? 'Password invalid' : '';
  return isUsernameValid && isPasswordValid;
};

const handleLogin = async () => {
  if (!isInputValid()) {
    return;
  }
  const isLoginSuccessful = await authStore.login(username.value, password.value);
  if (isLoginSuccessful) {
    showErrorMessage.value = false;
    router.push('/');
  } else {
    showErrorMessage.value = true;
  }
};

const resetErrorMessages = () => {
  usernameErrorMessage.value = '';
  passwordErrorMessage.value = '';
  showErrorMessage.value = false;
};
</script>

<template>
  <div class="flex min-h-screen flex-1 flex-col justify-center px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Log in to your account</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
      <div class="space-y-2" >
        <div>
          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Username</label>
          <div class="mt-2">
            <input id="username" name="username" autocomplete="username" required="true" v-model="username"
            class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset
            ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600
            sm:text-sm sm:leading-6" @input="resetErrorMessages" @keyup.enter="handleLogin" />
            <div class="h-2 mt-1 text-xs text-red-500">
              <p :class="usernameErrorMessage ? 'block' : 'hidden'">{{ usernameErrorMessage}}</p>
            </div>
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between">
            <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
          </div>
          <div class="mt-2">
            <input id="password" name="password" type="password" autocomplete="current-password" required="true" v-model="password"
            class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300
            placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
            @input="resetErrorMessages" @keyup.enter="handleLogin" />
            <div class="h-2 mt-1 text-xs text-red-500">
              <p :class="passwordErrorMessage ? 'block' : 'hidden'">{{ passwordErrorMessage }}</p>
            </div>
          </div>
        </div>

        <div class="pt-8">
          <button class="flex w-full justify-center rounded-md bg-black px-3 py-1.5 text-sm
          font-semibold leading-6 text-white shadow-sm focus-visible:outline focus-visible:outline-2
          focus-visible:outline-offset-2 focus:bg-opacity-80" @click="handleLogin">
            LOG IN
          </button>
          <div class="h-6 mt-1 text-sm text-center text-red-500">
            <p :class="showErrorMessage ? 'block' : 'hidden'">Invalid credentials</p>
          </div>
        </div>
      </div>

      <p class="flex justify-center gap-x-2 mt-4 text-center text-sm text-gray-500">
        <p class="my-auto">Not a member?</p>
        <router-link to="/register">
          <p class="font-semibold leading-6 text-violet-500 hover:text-violet-600">Register</p>
        </router-link>
        
      </p>
    </div>
  </div>
</template>

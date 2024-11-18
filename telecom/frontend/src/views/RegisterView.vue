<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.store';

const authStore = useAuthStore();

const name = ref('');
const username = ref('');
const password = ref('');
const confirmPassword = ref('');

const nameErrorMessage = ref('');
const usernameErrorMessage = ref('');
const passwordErrorMessage = ref('');
const confirmPasswordErrorMessage = ref('');
const showErrorMessage = ref(false);

const isSuccessful = ref(false);

const isStringNonEmpty = (text) => {
  return text && text.trim().length > 0;
};

const isInputValid = () => {
  const isNameValid = isStringNonEmpty(name.value);
  nameErrorMessage.value = isNameValid ? '' : 'Name invalid';
  const isUsernameValid = isStringNonEmpty(username.value);
  usernameErrorMessage.value = isUsernameValid ? '' : 'Username invalid';
  const isPasswordValid = isStringNonEmpty(password.value);
  passwordErrorMessage.value = isPasswordValid ? '' : 'Password invalid';
  const isConfirmPasswordValid = password.value === confirmPassword.value;
  confirmPasswordErrorMessage.value = isConfirmPasswordValid ? '' : 'Passwords do not match';
  return isNameValid && isUsernameValid && isPasswordValid && isConfirmPasswordValid;
};

const handleRegister = async () => {
  if (!isInputValid()) {
    return;
  }
  const isRegistrationSuccessful = await authStore.register({
    full_name: name.value.trim(),
    username: username.value.trim(),
    password: password.value.trim(),
  });
  if (isRegistrationSuccessful) {
    showErrorMessage.value = false;
    isSuccessful.value = true;
  } else {
    showErrorMessage.value = true;
  }
};

const resetErrorMessages = () => {
  nameErrorMessage.value = '';
  usernameErrorMessage.value = '';
  passwordErrorMessage.value = '';
  confirmPasswordErrorMessage.value = '';
  showErrorMessage.value = false;
};
</script>

<template>
  <div v-if="!isSuccessful" class="flex min-h-screen flex-1 flex-col justify-center px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Register for an account</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-lg">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-y-2 gap-x-4" action="#" method="POST">

        <div>
          <label for="name" class="block text-sm font-medium leading-6 text-gray-900">Full Name</label>
          <div class="mt-2">
            <input id="name" name="name" type="text" autocomplete="name" required="true" v-model="name"
            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset px-2
            ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
            @input="resetErrorMessages" />
          </div>
          <div class="h-2 text-xs text-red-500">
            <p :class="nameErrorMessage ? 'block' : 'hidden'">{{ nameErrorMessage }}</p>
          </div>
        </div>

        <div>
          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Username</label>
          <div class="mt-2">
            <input id="username" name="username" type="text" autocomplete="username" required="true" v-model="username"
            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset px-2
            ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
            @input="resetErrorMessages" />
          </div>
          <div class="h-2 mt-1 text-xs text-red-500">
            <p :class="usernameErrorMessage ? 'block' : 'hidden'">{{ usernameErrorMessage }}</p>
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
          <div class="mt-2">
            <input id="password" name="password" type="password" autocomplete="new-password" required="true" v-model="password"
            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset px-2
            ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
            @input="resetErrorMessages" />
          </div>
          <div class="h-2 mt-1 text-xs text-red-500">
            <p :class="passwordErrorMessage ? 'block' : 'hidden'">{{ passwordErrorMessage }}</p>
          </div>
        </div>

        <div>
          <label for="password_confirmation" class="block text-sm font-medium leading-6 text-gray-900">Repeat Password</label>
          <div class="mt-2">
            <input id="password_confirmation" name="password_confirmation" type="password" autocomplete="new-password" v-model="confirmPassword"
            required="true" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset px-2
            ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
            @input="resetErrorMessages" />
          </div>
          <div class="h-2 mt-1 text-xs text-red-500">
            <p :class="confirmPasswordErrorMessage ? 'block' : 'hidden'">{{ confirmPasswordErrorMessage }}</p>
          </div>
        </div>
        
        <div class="pt-6 md:col-start-2 md:mt-0 flex flex-col justify-end">
          <button class="flex w-full justify-center rounded-md bg-black py-1.5 text-sm
          font-semibold leading-6 text-white shadow-sm focus-visible:outline focus-visible:outline-2
          focus-visible:outline-offset-2 focus:bg-opacity-80 px-2" @click="handleRegister">
            REGISTER
          </button>
          <div class="h-2 mt-1 text-xs text-center text-red-500">
            <p :class="showErrorMessage ? 'block' : 'hidden'">Invalid input</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="flex min-h-[70vh] justify-center px-6 pt-12 pb-24 lg:px-8 mb-64">
    <div class="flex flex-col justify-center text-center">
      <div class="text-2xl">
        Registration successful!
      </div>
      <p>
        You can log in <RouterLink to="/login" class="font-bold hover:text-gray-500">here!</RouterLink>
      </p>
    </div>
  </div>
</template>

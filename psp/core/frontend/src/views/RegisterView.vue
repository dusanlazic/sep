<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.store';

const authStore = useAuthStore();

const name = ref('');
const username = ref('');
const password = ref('');
const confirmPassword = ref('');

const paymentSuccessUrl = ref('');
const paymentFailureUrl = ref('');
const paymentErrorUrl = ref('');
const paymentCallbackUrl = ref('');

const nameErrorMessage = ref('');
const usernameErrorMessage = ref('');
const passwordErrorMessage = ref('');
const confirmPasswordErrorMessage = ref('');

const paymentSuccessUrlErrorMessage = ref('');
const paymentFailureUrlErrorMessage = ref('');
const paymentErrorUrlErrorMessage = ref('');
const paymentCallbackUrlErrorMessage = ref('');

const showErrorMessage = ref(false);
const isSuccessful = ref(false);

const isStringNonEmpty = (text) => text && text.trim().length > 0;

const isValidUrl = (url) => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
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
  const isPaymentSuccessUrlValid = isValidUrl(paymentSuccessUrl.value);
  paymentSuccessUrlErrorMessage.value = isPaymentSuccessUrlValid ? '' : 'Invalid URL';
  const isPaymentFailureUrlValid = isValidUrl(paymentFailureUrl.value);
  paymentFailureUrlErrorMessage.value = isPaymentFailureUrlValid ? '' : 'Invalid URL';
  const isPaymentErrorUrlValid = isValidUrl(paymentErrorUrl.value);
  paymentErrorUrlErrorMessage.value = isPaymentErrorUrlValid ? '' : 'Invalid URL';
  const isPaymentCallbackUrlValid = isValidUrl(paymentCallbackUrl.value);
  paymentCallbackUrlErrorMessage.value = isPaymentCallbackUrlValid ? '' : 'Invalid URL';

  return (
    isNameValid &&
    isUsernameValid &&
    isPasswordValid &&
    isConfirmPasswordValid &&
    isPaymentSuccessUrlValid &&
    isPaymentFailureUrlValid &&
    isPaymentErrorUrlValid &&
    isPaymentCallbackUrlValid
  );
};

const handleRegister = async () => {
  if (!isInputValid()) {
    return;
  }
  const isRegistrationSuccessful = await authStore.register({
    title: name.value.trim(),
    username: username.value.trim(),
    password: password.value.trim(),
    payment_success_url: paymentSuccessUrl.value.trim(),
    payment_failure_url: paymentFailureUrl.value.trim(),
    payment_error_url: paymentErrorUrl.value.trim(),
    payment_callback_url: paymentCallbackUrl.value.trim(),
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
  paymentSuccessUrlErrorMessage.value = '';
  paymentFailureUrlErrorMessage.value = '';
  paymentErrorUrlErrorMessage.value = '';
  paymentCallbackUrlErrorMessage.value = '';
  showErrorMessage.value = false;
};
</script>

<template>
  <div class="flex min-h-screen flex-1 flex-col justify-center px-6 lg:px-8 bg-zinc-800">
    <div v-if="!isSuccessful" class="sm:mx-auto sm:w-full sm:max-w-lg">
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-zinc-300">Register for an account</h2>
      <div class="mt-10 grid grid-cols-1 md:grid-cols-2 gap-y-2 gap-x-4">
        
        <!-- Full Name -->
        <div>
          <label for="name" class="block text-sm font-medium leading-6 text-zinc-300">Name</label>
          <input id="name" v-model="name" placeholder="Title of your business" type="text" class="mt-2 w-full rounded-md px-2 py-1.5 text-zinc-800
          placeholder:text-zinc-400 shadow-sm outline-none focus:-outline-offset-2 focus:outline-zinc-300" @input="resetErrorMessages" />
          <div class="h-2 text-xs text-red-400">
            <p :class="nameErrorMessage ? 'block' : 'hidden'">{{ nameErrorMessage }}</p>
          </div>
        </div>

        <!-- Username -->
        <div>
          <label for="username" class="block text-sm font-medium leading-6 text-zinc-300">Username</label>
          <input id="username" v-model="username" placeholder="Your username" type="text" class="mt-2 w-full rounded-md px-2 py-1.5 text-zinc-800 
          placeholder:text-zinc-400 shadow-sm outline-none focus:-outline-offset-2 focus:outline-zinc-300" @input="resetErrorMessages" />
          <div class="h-2 mt-1 text-xs text-red-400">
            <p :class="usernameErrorMessage ? 'block' : 'hidden'">{{ usernameErrorMessage }}</p>
          </div>
        </div>

        <!-- Password -->
        <div>
          <label for="password" class="block text-sm font-medium leading-6 text-zinc-300">Password</label>
          <input id="password" v-model="password" placeholder="Your password" type="password" class="mt-2 w-full rounded-md px-2 py-1.5 text-zinc-800 
          placeholder:text-zinc-400 shadow-sm outline-none focus:-outline-offset-2 focus:outline-zinc-300" @input="resetErrorMessages" />
          <div class="h-2 mt-1 text-xs text-red-400">
            <p :class="passwordErrorMessage ? 'block' : 'hidden'">{{ passwordErrorMessage }}</p>
          </div>
        </div>

        <!-- Repeat Password -->
        <div>
          <label for="password_confirmation" class="block text-sm font-medium leading-6 text-zinc-300">Repeat Password</label>
          <input id="password_confirmation" v-model="confirmPassword" placeholder="Repeat your password" type="password" class="mt-2 w-full rounded-md px-2 py-1.5 text-zinc-800 
          placeholder:text-zinc-400 shadow-sm outline-none focus:-outline-offset-2 focus:outline-zinc-300" @input="resetErrorMessages" />
          <div class="h-2 mt-1 text-xs text-red-400">
            <p :class="confirmPasswordErrorMessage ? 'block' : 'hidden'">{{ confirmPasswordErrorMessage }}</p>
          </div>
        </div>

        <!-- Payment Success URL -->
        <div class="md:col-span-2">
          <label for="payment_success_url" class="block text-sm font-medium leading-6 text-zinc-300">Payment Success URL</label>
          <input id="payment_success_url" v-model="paymentSuccessUrl" placeholder="https://example.com/payment/success" type="url"
            class="mt-2 w-full rounded-md px-2 py-1.5 text-zinc-800 placeholder:text-zinc-400 shadow-sm outline-none focus:-outline-offset-2 focus:outline-zinc-300"
            @input="resetErrorMessages" />
          <div class="h-2 mt-1 text-xs text-red-400">
            <p :class="paymentSuccessUrlErrorMessage ? 'block' : 'hidden'">{{ paymentSuccessUrlErrorMessage }}</p>
          </div>
        </div>
        
        <!-- Payment Failure URL -->
        <div class="md:col-span-2">
          <label for="payment_failure_url" class="block text-sm font-medium leading-6 text-zinc-300">Payment Failure URL</label>
          <input id="payment_failure_url" v-model="paymentFailureUrl" placeholder="https://example.com/payment/failure" type="url"
            class="mt-2 w-full rounded-md px-2 py-1.5 text-zinc-800 placeholder:text-zinc-400 shadow-sm outline-none focus:-outline-offset-2 focus:outline-zinc-300"
            @input="resetErrorMessages" />
          <div class="h-2 mt-1 text-xs text-red-400">
            <p :class="paymentFailureUrlErrorMessage ? 'block' : 'hidden'">{{ paymentFailureUrlErrorMessage }}</p>
          </div>
        </div>
        
        <!-- Payment Error URL -->
        <div class="md:col-span-2">
          <label for="payment_error_url" class="block text-sm font-medium leading-6 text-zinc-300">Payment Error URL</label>
          <input id="payment_error_url" v-model="paymentErrorUrl" placeholder="https://example.com/payment/error" type="url"
            class="mt-2 w-full rounded-md px-2 py-1.5 text-zinc-800 placeholder:text-zinc-400 shadow-sm outline-none focus:-outline-offset-2 focus:outline-zinc-300"
            @input="resetErrorMessages" />
          <div class="h-2 mt-1 text-xs text-red-400">
            <p :class="paymentErrorUrlErrorMessage ? 'block' : 'hidden'">{{ paymentSuccessUrlErrorMessage }}</p>
          </div>
        </div>
        
        <!-- Payment Callback URL -->
        <div class="md:col-span-2">
          <label for="payment_callback_url" class="block text-sm font-medium leading-6 text-zinc-300">Payment Callback URL</label>
          <input id="payment_callback_url" v-model="paymentCallbackUrl" placeholder="https://api.example.com/payment/callback" type="url"
            class="mt-2 w-full rounded-md px-2 py-1.5 text-zinc-800 placeholder:text-zinc-400 shadow-sm outline-none focus:-outline-offset-2 focus:outline-zinc-300"
            @input="resetErrorMessages" />
          <div class="h-2 mt-1 text-xs text-red-400">
            <p :class="paymentCallbackUrlErrorMessage ? 'block' : 'hidden'">{{ paymentCallbackUrlErrorMessage }}</p>
          </div>
        </div>

        <!-- Register Button -->
        <div class="md:col-start-2 mt-6">
          <button @click="handleRegister" class="w-full rounded-md bg-red-400 text-zinc-800 px-3 py-2 text-sm 
          font-semibold hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">
            REGISTER
          </button>
          <div class="h-2 mt-1 text-xs text-center text-red-400">
            <p :class="showErrorMessage ? 'block' : 'hidden'">Invalid input</p>
          </div>
        </div>

      </div>
    </div>

    <!-- Success Message -->
    <div v-else class="flex flex-col items-center">
      <h2 class="text-2xl text-zinc-300">Registration successful!</h2>
      <router-link to="/login" class="mt-2 text-red-400 hover:text-red-500">Log in here!</router-link>
    </div>
  </div>
</template>

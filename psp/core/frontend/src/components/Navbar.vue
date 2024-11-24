<script setup>
import { ref } from 'vue';

const isPaymentPage = ref(window.location.href.includes('/payment'));
</script>

<template>
  <nav class="absolute top-0 right-left w-full">
    <div class="container px-4 sm:px-12 py-3 flex items-center justify-between">
      <RouterLink to="/" class="flex space-x-3">
        <img src="/logo.png" class="w-12 h-12"/>
        <p class="font-medium text-xl text-red-400 my-auto pb-2">pspspsps</p>
      </RouterLink>
      
      <div v-if="!isPaymentPage">
        <!-- <div v-if="!authStore.isUserLoggedIn()"> -->
        <div v-if="true">
          <RouterLink
            to="/login"
          >
            <button class="px-4 py-1 text-zinc-100 font-medium border border-zinc-100 border-dashed rounded hover:bg-red-400 hover:bg-opacity-80 text-sm">Log In</button>
          </RouterLink>
        </div>

        <div v-else class="flex space-x-8">
          <RouterLink to="/account" class="text-xs font-medium tracking-wider text-gray-500 hover:text-black">
            ACCOUNT
          </RouterLink>
          <button class="text-xs font-medium tracking-wider text-gray-500 hover:text-black">
            LOG OUT
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.store';
import { useRouter } from 'vue-router';

const router = useRouter();

const authStore = useAuthStore();

const handleLogout = async () =>{
  await authStore.logout();
  router.push('/');
};

const isPaymentPage = ref(window.location.href.includes('/payment'));
</script>

<template>
  <nav class="absolute top-0 right-left w-full">
    <div class="flex w-full px-4 sm:px-12 py-3 items-center justify-between">
      <RouterLink to="/" class="flex space-x-3">
        <img src="/logo.png" class="w-12 h-12"/>
        <p class="font-medium text-xl text-red-400 my-auto pb-2">pspspsps</p>
      </RouterLink>
      
      <div v-if="!isPaymentPage">
        <div v-if="!authStore.isUserLoggedIn()">
          <RouterLink
            to="/login"
          >
            <button class="px-4 py-1 text-zinc-200 font-medium border border-zinc-500 border-dashed rounded
             hover:border-zinc-300 hover:text-zinc-50 hover:bg-opacity-80 text-sm">Log In</button>
          </RouterLink>
        </div>

        <div v-else class="flex space-x-8">
          <RouterLink to="/account" class="text-xs font-medium tracking-wider text-zinc-500 hover:text-zinc-100">
            ACCOUNT
          </RouterLink>
          <button @click="handleLogout" class="text-xs font-medium tracking-wider text-zinc-500 hover:text-zinc-100">
            LOG OUT
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

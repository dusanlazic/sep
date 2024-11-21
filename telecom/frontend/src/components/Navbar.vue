<script setup>
import { useAuthStore } from '@/stores/auth.store';
import { useRouter } from 'vue-router';

const router = useRouter();
const authStore = useAuthStore();

const handleLogout = async () =>{
  await authStore.logout();
  router.push('/');
};
</script>

<template>
  <nav class="absolute top-0 right-left w-full bg-white shadow z-10">
    <div class="container mx-auto px-6 py-3 flex items-center justify-between">
      <RouterLink to="/" class="font-medium text-xl text-violet-500">
        Telecom Serbia
      </RouterLink>
      <div v-if="!authStore.isUserLoggedIn()">
        <RouterLink
          to="/login"
        >
          <button class="px-4 py-1 text-black font-medium border border-black border-dashed rounded hover:bg-violet-300 text-sm">Log In</button>
        </RouterLink>
      </div>

      <div v-else class="flex space-x-8">
        <RouterLink to="/account" class="text-xs font-medium tracking-wider text-gray-500 hover:text-black">
          ACCOUNT
        </RouterLink>
        <button @click="handleLogout" class="text-xs font-medium tracking-wider text-gray-500 hover:text-black">
          LOG OUT
        </button>
      </div>
    </div>
  </nav>
</template>

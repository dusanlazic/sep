<script setup>
import QrcodeVue from 'qrcode.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
</script>

<template>
  <div class="flex items-center justify-center h-screen bg-zinc-800">
    <div v-if="!route.query?.data" class="text-center">
      <h1 class="text-2xl font-bold text-red-500">Invalid Transaction</h1>
      <p class="text-zinc-400 mt-2">
        The IPS data is invalid or missing.
      </p>
    </div>
    <div v-else class="flex flex-col">
      <div class="p-2 rounded-md bg-white w-min mx-auto">
        <qrcode-vue :value="route.query.data" :size="240" level="H" render-as="svg" />
      </div>
      <p class="text-lg text-center mt-3 font-medium text-white">Scan the IPS code to proceed with your payment.</p>
    </div>
  </div>
</template>

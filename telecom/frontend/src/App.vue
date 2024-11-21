<script setup>
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';
import { useSubscriptionStore } from './stores/subscription.store';
import { onBeforeMount } from 'vue';

const subsciptionStore = useSubscriptionStore();

onBeforeMount(() => {
  if (subsciptionStore.offers.length == 0) {
    subsciptionStore.fetchOffers();
  }
});
</script>

<template>
  <Navbar />
  <RouterView />
</template>

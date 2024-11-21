<script setup>
import { ref, computed } from 'vue';
import Offer from '../components/services/Offer.vue';
import { useSubscriptionStore } from '@/stores/subscription.store';
import { onBeforeMount } from 'vue';

const subsciptionStore = useSubscriptionStore();

const offers = ref([]);
const selectedOffer = ref(null)

onBeforeMount(async () => {
  if (!subsciptionStore.offers?.length) {
    await subsciptionStore.fetchOffers();
  }

  offers.value = subsciptionStore.offers;

  if (offers.value && offers.value.length > 0) {
    selectedOffer.value = offers.value[0];
  }
});

const handlePlaceOrder = () => {
  // TODO: do
};

</script>

<template>
  <div v-if="offers && selectedOffer" class="h-full w-full flex flex-col justify-center px-4 md:px-24 lg:px-44 xl:px-72 my-20 select-none">
    <div class="text-xl mb-4 tracking-wide">Choose your offer</div>
    <div class="flex flex-col mx-auto p-4 sm:p-10 lg:p-12 bg-slate-100 rounded-lg gap-y-4">
      <div v-for="offer in offers">
        <Offer :offer="offer" @onSelect="selectedOffer = offer" :isSelected="offer === selectedOffer"/>
      </div>
    </div>
    <div class="flex flex-row justify-between h-24 mt-4">
      <div v-if="!!selectedOffer.price" class="text-right bg-slate-100 px-4 h-12 rounded-lg flex flex-col justify-center">
        <div class="font-bold">Yearly €{{ selectedOffer.price }}</div>
      </div>
      <button v-if="!!selectedOffer" @click="handlePlaceOrder"
        class="text-accent text-lg font-bold border border-dashed border-black hover:bg-violet-300 tracking-wide px-6 h-12 rounded-lg">
        Pay │ €{{ selectedOffer.price  }}
      </button>
    </div>
  </div>
  <div v-else class="h-full min-h-screen w-full flex flex-col justify-center text-center text-gray-400">
    No offers at the moment.
  </div>
</template>

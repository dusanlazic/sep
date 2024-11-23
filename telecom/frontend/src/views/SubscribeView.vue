<script setup>
import { ref } from 'vue';
import Offer from '../components/services/Offer.vue';
import { useSubscriptionStore } from '@/stores/subscription.store';
import { onBeforeMount } from 'vue';

const subsciptionStore = useSubscriptionStore();

const offers = ref([]);
const selectedOffer = ref(null);
const subscriptionDuration = ref(1);
const autoRenew = ref(false);

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
  console.log(
    `Subscribe: ${selectedOffer.value.identifier}, Duration: ${subscriptionDuration.value} year(s), Auto-renew: ${autoRenew.value}`
  );

  subsciptionStore.subscribeToOffer({
    offer_identifier: selectedOffer.value.identifier,
    duration_in_years: subscriptionDuration.value,
    auto_renew: autoRenew.value,
  })

};

const handleDurationChange = (duration) => {
  subscriptionDuration.value = duration;
};
</script>

<template>
  <div
    v-if="offers && selectedOffer"
    class="h-full w-full flex flex-col justify-center px-4 md:px-24 lg:px-44 xl:px-72 my-20 select-none"
  >
    <div class="text-xl mb-4 tracking-wide">Choose your offer</div>
    <div class="flex flex-col mx-auto p-4 sm:p-8 bg-slate-100 rounded-lg gap-y-4">
      <div v-for="offer in offers" :key="offer.identifier">
        <Offer
          :offer="offer"
          @onSelect="selectedOffer = offer"
          :isSelected="offer === selectedOffer"
        />
      </div>

      <!-- Subscription Duration Buttons -->
      <div class="flex flex-row gap-2 mt-4">
        <button
          v-for="year in 5"
          :key="year"
          :class="[
            'px-4 py-2 border rounded text-sm font-medium',
            subscriptionDuration === year
              ? 'bg-violet-600 text-white'
              : 'bg-white text-black border-gray-400 hover:bg-violet-200'
          ]"
          @click="handleDurationChange(year)"
        >
          {{ year }} Year<span v-if="year > 1">s</span>
        </button>
      </div>

      <!-- Auto-Renew Checkbox -->
      <div class="flex items-center mt-3">
        <input
          type="checkbox"
          id="autoRenew"
          v-model="autoRenew"
          class="h-5 w-5 rounded border-gray-300 text-violet-500 focus:ring-violet-500 accent-violet-600"
        />
        <label for="autoRenew" class="ml-2 text-gray-700 text-sm">
          Auto-renew
        </label>
      </div>
    </div>

    <!-- Pay Button -->
    <div class="flex flex-row justify-end h-24 mt-4">
      <button
        v-if="!!selectedOffer"
        @click="handlePlaceOrder"
        class="text-accent text-lg font-bold border border-dashed border-black hover:bg-violet-300 tracking-wide px-6 h-12 rounded-lg"
      >
        Pay │ €{{ selectedOffer.price * subscriptionDuration }}
      </button>
    </div>
  </div>

  <div
    v-else
    class="h-full min-h-screen w-full flex flex-col justify-center text-center text-gray-400"
  >
    No offers at the moment.
  </div>
</template>

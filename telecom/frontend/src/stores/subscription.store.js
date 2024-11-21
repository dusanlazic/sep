import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ax } from '@/utils/axios';

export const useSubscriptionStore = defineStore('subscriptions', () => {
  const offers = ref([]);
  
  async function fetchOffers() {
    try {
      const response = await ax.get(
        '/offers',
      );
      const offersResponse = response.data;
      

      if (offersResponse) {
        offers.value = offersResponse;
      }

      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  function clearOffers() {
    offers.value = [];
  };

  return { offers, fetchOffers, clearOffers };
});

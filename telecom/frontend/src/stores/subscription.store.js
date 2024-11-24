import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ax } from '@/utils/axios';

export const useSubscriptionStore = defineStore('subscriptions', () => {
  const offers = ref([]);
  const subscriptions = ref([]);
  
  async function fetchOffers() {
    try {
      const response = await ax.get(
        '/offers',
      );
      const data = response.data;
      

      if (data) {
        offers.value = data;
      }

      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  async function fetchSubscriptions() {
    try {
      const response = await ax.get(
        '/offers/subscriptions',
      );
      const data = response.data;
      
      if (data) {
        subscriptions.value = data;
      }

      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  async function subscribeToOffer(data) {
    try {
      const response = await ax.post(
        '/offers/subscriptions',
        data,
      );
      const responseData = response?.data;
      
      console.log('SUB', responseData);

      if (responseData && responseData.payment_url) {
        window.location.href = responseData.payment_url;
      }

      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  function getActiveSubscription() {
    return subscriptions.value.find((sub) => new Date() < new Date(sub.end_date));
  };

  function clearOffers() {
    offers.value = [];
  };

  return { offers, subscriptions, fetchOffers, clearOffers, subscribeToOffer, fetchSubscriptions, getActiveSubscription };
});

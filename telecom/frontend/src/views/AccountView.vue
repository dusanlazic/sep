<script setup>
import { useAuthStore } from '@/stores/auth.store';
import { useSubscriptionStore } from '@/stores/subscription.store';
import { onBeforeMount, ref } from 'vue';

const authStore = useAuthStore();
const subsciptionStore = useSubscriptionStore();

const isLoaded = ref(false);
const subscriptions = ref([]);
const activeSubscription = ref(null);
const username = ref('');

const formatDate = (date) => new Date(date).toLocaleDateString();

onBeforeMount(async () => {
  await subsciptionStore.fetchSubscriptions();
  activeSubscription.value = subsciptionStore.getActiveSubscription();
  subscriptions.value = subsciptionStore.subscriptions;
  username.value = authStore.session?.username || 'Guest';
  isLoaded.value = true;
});
</script>

<template>
  <div class="flex flex-col w-full px-44 mt-24">
    
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Welcome, {{ username }}</h1>
    </div>

    <div v-if="isLoaded && subscriptions?.length">
      <div v-if="activeSubscription" class="mb-8">
        <div class="text-2xl font-bold mb-4">Your Active Subscription</div>
        <div class="flex flex-col w-full mx-auto p-6 bg-violet-100 border border-violet-300 rounded-lg gap-y-4 shadow-lg">
          <div class="text-lg">
            <strong>Offer:</strong> {{ activeSubscription.title }}
          </div>
          <div class="text-gray-600 text-sm">
            {{ activeSubscription.description }}
          </div>
          <div class="text-gray-700">
            <strong>Price:</strong> €{{ activeSubscription.price * activeSubscription.duration_in_years }}
          </div>
          <div class="text-gray-700">
            <strong>Start Date:</strong> {{ formatDate(activeSubscription.start_date) }}
          </div>
          <div class="text-gray-700">
            <strong>End Date:</strong> {{ formatDate(activeSubscription.end_date) }}
          </div>
          <div class="flex items-center">
            <strong class="mr-2">Auto-renew:</strong>
            <span
              :class="[ 
                'px-2 py-1 rounded-full text-sm font-medium', 
                activeSubscription.auto_renew ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600' 
              ]"
            >
              {{ activeSubscription.auto_renew ? 'Enabled' : 'Disabled' }}
            </span>
          </div>
        </div>
      </div>

      <div>
        <div class="text-xl font-bold mb-4">Inactive Subscriptions</div>
        <div v-if="subscriptions.length > 1" class="grid gap-4">
          <div
            v-for="subscription in subscriptions.filter((sub) => sub !== activeSubscription)"
            :key="subscription.offer_identifier"
            class="flex flex-col w-full mx-auto p-6 bg-gray-100 border border-gray-300 rounded-lg gap-y-4 shadow"
          >
            <div class="text-lg">
              <strong>Offer:</strong> {{ subscription.title }}
            </div>
            <div class="text-gray-600 text-sm">
              {{ subscription.description }}
            </div>
            <div class="text-gray-700">
              <strong>Price:</strong> €{{ subscription.price * subscription.duration_in_years }}
            </div>
            <div class="text-gray-700">
              <strong>Start Date:</strong> {{ formatDate(subscription.start_date) }}
            </div>
            <div class="text-gray-700">
              <strong>End Date:</strong> {{ formatDate(subscription.end_date) }}
            </div>
            <div class="flex items-center">
              <strong class="mr-2">Auto-renew:</strong>
              <span
                :class="[ 
                  'px-2 py-1 rounded-full text-sm font-medium', 
                  subscription.auto_renew ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600' 
                ]"
              >
                {{ subscription.auto_renew ? 'Enabled' : 'Disabled' }}
              </span>
            </div>
          </div>
        </div>
        <div v-else class="text-gray-500 text-center">No inactive subscriptions.</div>
      </div>
    </div>

    <div v-else class="text-center text-gray-500">
      No subscriptions found.
    </div>
  </div>
</template>

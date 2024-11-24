<script setup>
import { getTransaction } from '@/services/transaction.service';
import QrcodeVue from 'qrcode.vue';
import { onBeforeMount, ref } from 'vue';
import { useRoute } from 'vue-router';

const isValidUUID = (id) => /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$/.test(id);

const route = useRoute();

const isInvalidTransaction = ref(false);
const isLoaded = ref(false);
const transaction = ref();

const fetchTransaction = async (id) => {
  transaction.value = await getTransaction(id);
};

onBeforeMount(async () => {
  const id = route.query.id || null;
  isInvalidTransaction.value = !id || !isValidUUID(id);

  if (!isInvalidTransaction.value) {
    await fetchTransaction(id);
  }

  startCheckingForPayment(id);
  isLoaded.value = true;
});

const checkStatusChange = (interval) => {
  if (transaction.value.status === 'failed') {
    clearInterval(interval);
    window.location.href = transaction.value.urls.failure;
  } else if (transaction.value.status === 'completed') {
    clearInterval(interval);
    window.location.href = transaction.value.urls.success;
  }
};

const startCheckingForPayment = (id) => {
  const interval = setInterval(async () => {
    await fetchTransaction(id);
    checkStatusChange(interval);
  }, 5000);
};
</script>

<template>
  <div class="flex items-center justify-center h-screen bg-zinc-800">
    <div v-if="isInvalidTransaction" class="text-center">
      <h1 class="text-2xl font-bold text-red-500">Invalid Transaction</h1>
      <p class="text-zinc-400 mt-2">
        The transaction ID is invalid or missing.
      </p>
    </div>
    <div v-else-if="isLoaded && !isInvalidTransaction" class="flex flex-col">
      <div class="p-2 rounded-md bg-zinc-300">
        <qrcode-vue :value="transaction.deposit_address" :size="240" level="H" render-as="svg" />
      </div>
      <p class="text-lg text-center mt-3 font-medium text-white">{{ transaction.amount }} to pay in Bitcoin</p>
    </div>
  </div>
</template>

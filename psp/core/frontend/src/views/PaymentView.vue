<script setup>
import { useRoute } from 'vue-router';
import { ref, onBeforeMount } from 'vue';
import { getTransaction, proceedWithTransaction } from '@/services/transaction.service';

const isValidUUID = (id) => /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$/.test(id);

const route = useRoute();
const isInvalidTransaction = ref(false);
const isPaymentInProgress = ref(false);
const paymentMethods = ref([]);

const isLoaded = ref(false);
const transaction = ref();

onBeforeMount(async () => {
  const id = route.query.transaction_id || null;
  isInvalidTransaction.value = !id || !isValidUUID(id);

  if (!isInvalidTransaction.value) {
    transaction.value = await getTransaction(id);
    paymentMethods.value = transaction?.value?.payment_methods?.map((m) => {
      return {
        name: m,
      }
    });
  }

  isLoaded.value = true;
});

const handleChooseMethod = async (method) => {
  isPaymentInProgress.value = true;
  await proceedWithTransaction(transaction.value.id, method);
  isPaymentInProgress.value = false;
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

    <div v-else-if="isLoaded && transaction && !isPaymentInProgress" class="flex justify-center">
      <div class="flex flex-col justify-between min-h-120 w-96 bg-zinc-700 rounded-xl p-6">
        <div>
          <p class="text-xl md:text-3xl font-medium text-red-400">{{ transaction.subject }}</p>
          <p class="text-zinc-300 text-sm mt-4">{{ transaction.description }}</p>
        </div>
        <div class="flex justify-between h-16 border-b border-dashed border-zinc-500">
          <p class="text-xl font-bold text-zinc-300 mt-auto">Total</p>
          <p class="text-xl font-bold text-zinc-300 mt-auto">€{{ transaction.amount }}</p>
        </div>
      </div>
      
      <div class="flex flex-col text-white p-6 w-96">
        <div class="flex flex-col select-none">
          <div class="text-xl md:text-3xl text-zinc-300 font-medium">Pay with</div>
          <div v-if="paymentMethods.length" class="flex flex-col space-y-4 mt-4 w-full">
            <div v-for="method in paymentMethods">
              <div class="flex gap-x-6 px-6 py-4 hover:bg-stone-700 hover:bg-opacity-30 hover:text-red-400
              cursor-pointer bg-panel border border-black bg-zinc-700 rounded-lg shadow-inner"
              @click="handleChooseMethod(method.name)">
                <div class="shrink-0">
                  <img :src="`/icons/${method.name}.png`" :alt="method.name" class="h-11 w-11 object-contain shrink-0">
                </div>
                <div class="tracking-wider uppercase my-auto text-lg font-medium">
                  {{ method.name.replaceAll('_', ' ') }}
                </div>
              </div>
            </div>
          </div>
          <div v-else class="animate-spin w-16 h-16 text-4xl mx-auto mt-20">
            .
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="!isInvalidTransaction && isLoaded && isPaymentInProgress">
      <div class="animate-spin w-16 h-16 text-4xl mx-auto text-red-400">
        .
      </div>
      <p class="text-2xl text-zinc-200 mt-4 text-center">Processing your payment</p>
    </div>

    <div v-else-if="!isLoaded">
      <div class="animate-spin w-16 h-16 text-4xl mx-auto text-zinc-300">
        .
      </div>
      <p class="text-2xl text-zinc-300 mt-2">Loading...</p>
    </div>

    <div v-else class="text-center">
      <h1 class="text-2xl font-bold text-zinc-200">Not Found</h1>
      <p class="text-zinc-400 mt-2">
        Transaction does not exist.
      </p>
    </div>
  </div>
</template>

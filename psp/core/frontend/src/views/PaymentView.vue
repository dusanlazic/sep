<script setup>
import { useRoute } from 'vue-router';
import { ref, onBeforeMount } from 'vue';

const isValidUUID = (id) => /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$/.test(id);

const route = useRoute();
const transactionId = ref(null);
const isInvalidTransaction = ref(false);
const paymentMethods = ref([
  {
    name: "CARD",
  },
  {
    name: "PAYPAL",
  }
]);

onBeforeMount(() => {
  const id = route.query.transaction_id || null;
  transactionId.value = id;
  isInvalidTransaction.value = !id || !isValidUUID(id);
});

</script>

<template>
  <div class="flex items-center justify-center h-screen bg-zinc-800">
    <div v-if="isInvalidTransaction" class="text-center">
      <h1 class="text-2xl font-bold text-red-600">Invalid Transaction</h1>
      <p class="text-gray-600 mt-2">
        The transaction ID is invalid or missing.
      </p>
    </div>

    <div v-else>
      <div class="flex flex-col justify-center h-full w-full text-white px-4 sm:px-24 md:px-32 lg:px-40 xl:px-64 py-20">

        <div class="flex flex-col select-none">
          <div class="text-xl md:text-2xl w-72 text-center mx-auto">Choose your preferred method of payment</div>
          <div class="flex flex-col gap-4 mt-6 w-80">
            <div v-for="method in paymentMethods">
              <div class="flex gap-x-6 px-6 py-4 hover:bg-stone-700 hover:bg-opacity-30 cursor-pointer bg-panel border border-black bg-zinc-700 rounded-lg shadow-inner"
              @click="handleChooseMethod(method.name)">
                <div class="shrink-0">
                  <img :src="`../src/assets/icons/${method.name}.png`" :alt="method.name" class="h-11 w-11 object-contain shrink-0">
                </div>
                <div class="tracking-wider uppercase my-auto">
                  {{ method.name.replaceAll('_', ' ') }}
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

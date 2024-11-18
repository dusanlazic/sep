<script setup>
import { ref, computed } from 'vue'
import Service from '../components/services/Service.vue'

const services = ref([]);

getServices(
  (data) => {
    services.value = data.map((d) => {return {...d, price: Number(d.price), isSelected: false}})
  },
  () => {
    // boo hoo
  });

const handlePlaceOrder = () => {
  if (services.value.some((s) => s.isSelected)) {
    placeOrder(
      services.value.filter((s) => s.isSelected).map((s) => s.id),
      (loc) => {
        window.open(loc, '_self');
      },
      () => {
        // boo hoo
      });
  }
}

const totalMonthlyPrice = computed(() => {
  return services.value.reduce((a, c) => {
    if (c.isSelected) {
      return a + c.price
    } else {
      return a;
    }
  }, 0)
})

</script>

<template>
  <div class="h-full w-full flex flex-col justify-center px-4 md:px-24 lg:px-64 xl:px-80 my-20 select-none">
    <div class="font-bold text-xl mb-4 tracking-wide">Izaberite željene opcije</div>
    <div class="flex flex-col mx-auto p-4 sm:p-10 lg:p-20 bg-slate-100 rounded-lg gap-y-4">
      <div v-for="service in services">
        <service :service="service"/>
      </div>
    </div>
    <div class="flex flex-row justify-between h-24 mt-4">
      <div v-if="services.some(x => x.isSelected)" class="text-right bg-slate-100 px-4 h-16 rounded-lg flex flex-col justify-center">
        <div class="font-bold">Godišnje {{ totalMonthlyPrice * 12 }}</div>
        <div class="text-xs text-slate-700">(Mesečno {{ totalMonthlyPrice }}e)</div>
      </div>
      <button v-if="services.some(x => x.isSelected)" @click="handlePlaceOrder"
        class="bg-dark text-accent text-lg font-bold tracking-wide px-6 h-16 rounded-lg">
        Plati │ {{ totalMonthlyPrice * 12 }}e
      </button>
    </div>
  </div>
</template>

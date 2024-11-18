<script setup>
  import { defineProps } from 'vue'

  const props = defineProps({
    service: {
      type: Object,
      required: true,
    },
  })
</script>

<template>
  <div class="rounded-lg p-3 cursor-pointer"
  :class="[service.isSelected ? 'bg-dark': 'bg-white']"
  @click="service.isSelected = !service.isSelected">
    <div class="flex flex-row justify-between">
      <div class="font-bold text-sm tracking-wide"
        :class="[service.isSelected ? 'text-white': 'text-black']">
        {{ service.name }}
      </div>
      <div :class="[service.isSelected ? 'bg-accent rounded-full h-4 w-4': 'hidden']">

      </div>
    </div>
    <div class="flex flex-row justify-between">
      <div class="text-xs mt-0.5 w-4/5"
        :class="[service.isSelected ? 'text-slate-400': 'text-slate-500']">
        {{ service.description }}
      </div>
      <div class="text-right">
        <div class="text-sm font-bold" :class="[service.isSelected ? 'text-white': 'text-black']">
          Mesečno {{ service.price }}e
        </div>
        <div class="text-xs font-light" :class="[service.isSelected ? 'text-slate-300': 'text-slate-600']">
          Godišnje {{ service.price * 12 }}e
        </div>
      </div>
    </div>
  </div>
</template>

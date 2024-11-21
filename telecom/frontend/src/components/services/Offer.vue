<script setup>
  import { defineProps } from 'vue'

  const props = defineProps({
    offer: {
      type: Object,
      required: true,
    },
    isSelected: {
      type: Boolean,
      required: true,
      default: false,
    },
  });

  const emit = defineEmits(['onSelect']);

  const handleSelect = () => {
    emit('onSelect');
  };
</script>

<template>
  <div class="rounded-lg p-3 cursor-pointer"
  :class="[isSelected ? 'bg-violet-600': 'bg-white']"
  @click="handleSelect">
    <div class="flex flex-row justify-between">
      <div class="font-bold text-2xl tracking-wide"
        :class="[isSelected ? 'text-white' : 'text-black']">
        {{ offer.title }}
      </div>
      <div :class="[isSelected ? 'bg-accent rounded-full h-4 w-4': 'hidden']">

      </div>
    </div>
    <div class="flex flex-row justify-between">
      <div class="text-xs mt-0.5 w-3/5"
        :class="[isSelected ? 'text-sky-100': 'text-slate-500']">
        {{ offer.description }}
      </div>
      <div class="text-right flex flex-col justify-end">
        <div class="text-base font-medium" :class="[isSelected ? 'text-white': 'text-slate-600']">
          €{{ offer.price }}/year
        </div>
      </div>
    </div>
  </div>
</template>

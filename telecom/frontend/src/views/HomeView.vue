<script setup>
import { useAuthStore } from '@/stores/auth.store';
import { useRouter } from 'vue-router';

const router = useRouter();
const authStore = useAuthStore();

const goToSubscribe = () => {
  if (!authStore.isUserLoggedIn()) {
    router.push('/login');
  } else {
    router.push('/subscribe');
  }
};
</script>

<template>
  <div class="bg-gray-50">
    <header class="flex flex-col justify-center min-h-screen bg-[radial-gradient(#e5e7eb_1.5px,transparent_1.5px)] sm:bg-[radial-gradient(#e2e4e9_1px,transparent_1px)]
    [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_80%,transparent_100%)]">
      <div class="container mx-auto px-6 py-12 text-center">
        <h1 class="text-4xl font-bold">Welcome to<br><span class="text-violet-500 text-8xl">Telecom Serbia</span></h1>
        <p class="mt-2 text-lg">
          Experience lightning-fast internet and reliable telecom services tailored for you.
        </p>
        <button @click="goToSubscribe"
          class="mt-10 px-8 py-3 bg-white font-semibold rounded shadow hover:bg-violet-300 border-black border-dashed border"
        >
          Subscribe Now
        </button>
      </div>
    </header>

    <section class="container mx-auto px-6 py-28">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-gray-800">Why Choose Telecom Serbia?</h2>
        <p class="mt-2 text-gray-600">
          Discover the benefits of joining our network.
        </p>
      </div>
      <div class="grid gap-8 md:grid-cols-3">
        <div class="p-6 bg-white rounded shadow">
          <h3 class="text-xl font-bold text-black">Fast Internet</h3>
          <p class="mt-2 text-gray-600">
            Stream, browse, and work with blazing-fast internet speeds.
          </p>
        </div>
        <div class="p-6 bg-white rounded shadow">
          <h3 class="text-xl font-bold text-black">Affordable Plans</h3>
          <p class="mt-2 text-gray-600">
            Choose from a variety of plans that suit your budget.
          </p>
        </div>
        <div class="p-6 bg-white rounded shadow">
          <h3 class="text-xl font-bold text-black">24/7 Support</h3>
          <p class="mt-2 text-gray-600">
            Get assistance whenever you need it with our round-the-clock support.
          </p>
        </div>
      </div>
    </section>

    <section class="bg-gradient-to-br from-violet-400 to-violet-600 text-white shadow-inner">
      <div class="container mx-auto px-6 py-20 text-center">
        <h2 class="text-2xl font-bold">Ready to get started?</h2>
        <p class="mt-2">
          Join thousands of satisfied customers enjoying Telecom Serbia's services.
        </p>
          <button @click="goToSubscribe"
            class="mt-6 px-8 py-3 bg-white text-black font-semibold rounded shadow hover:bg-gray-100"
          >
            Subscribe Now
          </button>
      </div>
    </section>
  </div>
</template>

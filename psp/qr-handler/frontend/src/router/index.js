import { createRouter, createWebHistory } from 'vue-router';
import PaymentView from '@/views/PaymentView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/payment',
      name: 'payment-view',
      component: PaymentView,
    },
  ],
});

export default router;

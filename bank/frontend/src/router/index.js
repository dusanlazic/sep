import { createRouter, createWebHistory } from 'vue-router';
import CardPayView from '@/views/CardPayView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'card-pay',
      component: CardPayView
    },
  ]
})

export default router

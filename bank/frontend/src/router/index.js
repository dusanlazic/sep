import { createRouter, createWebHistory } from 'vue-router';
import CardPayView from '@/views/CardPayView.vue';
import NotFoundView from '@/views/NotFoundView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/payment',
      name: 'card-pay',
      component: CardPayView,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView,
    },
  ]
})

export default router

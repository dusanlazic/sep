import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import SubscribeView from '@/views/SubscribeView.vue';
import PaymentSuccessView from '@/views/PaymentSuccessView.vue';
import PaymentFailedView from '@/views/PaymentFailedView.vue';
import PaymentErrorView from '@/views/PaymentErrorView.vue';
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
import AccountView from '@/views/AccountView.vue';
import NotFoundView from '../views/NotFoundView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/account',
      name: 'account',
      component: AccountView,
    },
    {
      path: '/subscribe',
      name: 'subscribe',
      component: SubscribeView
    },
    {
      path: '/payments/success',
      name: 'payment-success',
      component: PaymentSuccessView
    },
    {
      path: '/payments/fail',
      name: 'payment-fail',
      component: PaymentFailedView
    },
    {
      path: '/payments/error',
      name: 'payment-error',
      component: PaymentErrorView
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView,
    },
  ],
})

export default router

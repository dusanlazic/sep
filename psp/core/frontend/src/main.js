import './assets/style.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import router from './router';

const pinia = createPinia();
const app = createApp(App);

app.use(router);

app.use(Toast, {});

app.use(pinia);
app.mount('#app');

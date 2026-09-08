import { createApp } from "vue";
import App from "./App.vue";
import vuetify from "/plugins/vuetify";
import router from "./router";
import { createPinia } from "pinia";

createApp(App).use(vuetify).use(router).use(createPinia()).mount("#app");

// import { createApp } from "vue";
// import App from "./App.vue";
// import vuetify from "./plugins/vuetify";
// import router from "./router";
// import { createPinia } from "pinia";

// createApp(App).use(vuetify).use(createPinia()).use(router).mount("#app");

import { createApp } from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "./router";
import { createPinia } from "pinia";

const app = createApp(App).use(vuetify).use(createPinia()).use(router);

app.mount("#app");

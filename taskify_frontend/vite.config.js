import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";
import vuetify from "vite-plugin-vuetify";

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue(), vuetify({ autoImport: true })],
    server: {
        host: "0.0.0.0",
        port: 5173,
        watch: {
            usePolling: true,
        },
    },
});

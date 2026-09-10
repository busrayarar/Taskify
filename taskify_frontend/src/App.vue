<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "./stores/auth";
import { useTheme } from "vuetify";

const drawer = ref(true);
const rail = ref(true);
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const theme = useTheme();

function handleLogout() {
    authStore.logout();
    router.push({ name: "Login" });
}

function toggleTheme() {
    theme.global.name.value = theme.global.current.value.dark
        ? "light"
        : "dark";
}
</script>

<template>
    <v-app>
        <template v-if="route.name === 'Login'">
            <!-- login sayfasında yalnızca router view göster -->
            <router-view />
        </template>

        <template v-else>
            <v-navigation-drawer v-model="drawer" :rail="rail" permanent>
                <v-list>
                    <v-list-item
                        :title="authStore.username"
                        prepend-icon="mdi-account-circle"
                        @click="rail = !rail"
                    >
                    </v-list-item>
                </v-list>

                <v-divider />

                <v-list density="compact" nav>
                    <v-list-item to="/" prepend-icon="mdi-home" title="Home" />
                    <v-list-item
                        v-if="authStore.isAdmin"
                        to="/users"
                        prepend-icon="mdi-account-group"
                        title="Users"
                    />
                    <v-list-item
                        to="/tasks"
                        prepend-icon="mdi-checkbox-marked-outline"
                        title="Tasks"
                    />
                </v-list>
            </v-navigation-drawer>

            <v-app-bar>
                <v-toolbar-title>Taskify</v-toolbar-title>
                <v-spacer />
                <v-btn
                    :icon="
                        theme.global.current.value.dark
                            ? 'mdi-weather-sunny'
                            : 'mdi-weather-night'
                    "
                    @click="toggleTheme"
                />
                <v-btn @click="handleLogout">Çıkış Yap</v-btn>
            </v-app-bar>

            <v-main>
                <router-view />
            </v-main>
        </template>
    </v-app>
</template>

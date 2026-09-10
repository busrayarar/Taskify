<template>
    <v-container class="fill-height" fluid>
        <v-row justify="center" align="center">
            <v-col cols="12" sm="6" md="4">
                <v-card class="pa-6">
                    <v-card-title>Giriş Yap</v-card-title>

                    <v-form @submit.prevent="handleLogin">
                        <v-text-field
                            v-model="username"
                            label="Kullanıcı Adı"
                            required
                        />
                        <v-text-field
                            v-model="password"
                            label="Şifre"
                            type="password"
                            required
                            name="password1"
                        />

                        <v-alert
                            v-if="errorMessage"
                            type="error"
                            density="compact"
                            class="mb-4"
                        >
                            {{ errorMessage }}
                        </v-alert>

                        <v-btn
                            type="submit"
                            color="primary"
                            block
                            :loading="loading"
                        >
                            Giriş Yap
                        </v-btn>
                    </v-form>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import api from "../api";

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false);

const router = useRouter();
const authStore = useAuthStore();

async function handleLogin() {
    errorMessage.value = "";
    loading.value = true;

    try {
        const response = await api.post("/login/", {
            username: username.value,
            password: password.value,
        });
        const isAdmin = response.data.is_staff || false;

        authStore.setAuth(
            response.data.access,
            username.value,
            response.data.user_id,
            isAdmin,
        );
        router.push({ name: "Home" });
    } catch (error) {
        errorMessage.value = "Kullanıcı adı veya şifre hatalı.";
    } finally {
        loading.value = false;
    }
}
</script>

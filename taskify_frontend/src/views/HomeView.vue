<script setup>
import { ref, onMounted } from "vue";
import api from "../api";

const stats = ref({
    //başlangıçta 3 sayaç da 0 tutan reactive değişken
    TODO: 0,
    IN_PROGRESS: 0,
    DONE: 0,
});

async function fetchStats() {
    try {
        const response = await api.get("/tasks/stats/");
        stats.value = response.data;
    } catch (error) {
        console.error("Sayaçlar alınamadı:", error);
    }
}

onMounted(() => {
    //home sayfasına her gelindiğinde sayaçlar backendden yeni çekilicek
    fetchStats();
});
</script>

<template>
    <v-container>
        <h1 class="mb-6">Anasayfa</h1>

        <v-row>
            <v-col cols="12" sm="4">
                <v-card class="pa-4" color="amber-lighten-4">
                    <v-card-title>TODO</v-card-title>
                    <v-card-text class="text-h3">{{ stats.TODO }}</v-card-text>
                </v-card>
            </v-col>

            <v-col cols="12" sm="4">
                <v-card class="pa-4" color="blue-lighten-4">
                    <v-card-title>IN PROGRESS</v-card-title>
                    <v-card-text class="text-h3">{{
                        stats.IN_PROGRESS
                    }}</v-card-text>
                </v-card>
            </v-col>

            <v-col cols="12" sm="4">
                <v-card class="pa-4" color="green-lighten-4">
                    <v-card-title>DONE</v-card-title>
                    <v-card-text class="text-h3">{{ stats.DONE }}</v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

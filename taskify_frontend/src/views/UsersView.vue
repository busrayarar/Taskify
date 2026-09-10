<script setup>
import { ref, onMounted } from "vue";
import api from "../api";

const users = ref([]);
const loading = ref(false);
const searchQuery = ref("");

const headers = [
    //tablo sütunları
    { title: "Kullanıcı Adı", key: "username" },
    { title: "Ad", key: "first_name" },
    { title: "Soyad", key: "last_name" },
    { title: "Email", key: "email" },
];

async function fetchUsers() {
    //get api users isteği
    loading.value = true;
    try {
        const response = await api.get("/users/", {
            params: { search: searchQuery.value },
        });
        users.value = response.data;
    } catch (error) {
        console.error("Kullanıcılar alınamadı:", error);
    } finally {
        loading.value = false;
    }
}

function handleSearch() {
    fetchUsers();
}

onMounted(() => {
    fetchUsers();
});
</script>

<template>
    <v-container>
        <h1 class="mb-4">Kullanıcılar</h1>

        <div class="d-flex justify-end mb-15">
            <v-text-field
                v-model="searchQuery"
                :loading="loading"
                append-inner-icon="mdi-magnify"
                density="compact"
                label="Kullanıcı ara"
                variant="solo"
                hide-details
                single-line
                @click:append-inner="handleSearch"
                @keyup.enter="handleSearch"
                style="max-width: 1000px"
            />
        </div>

        <v-data-table :headers="headers" :items="users" :loading="loading" />
    </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api";

const users = ref([]);
const loading = ref(false);
const searchQuery = ref("");
const addDialog = ref(false);
const saving = ref(false);
const addError = ref("");
const fieldErrors = ref({});
const editMode = ref(false);
const editingUserId = ref(null);
const newUser = ref({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    password_confirm: "",
});
const deleteDialog = ref(false);
const userToDelete = ref(null);
const deleting = ref(false);

const headers = [
    { title: "Kullanıcı Adı", key: "username" },
    { title: "Ad", key: "first_name" },
    { title: "Soyad", key: "last_name" },
    { title: "Email", key: "email" },
    { title: "Sil", key: "actions", sortable: false },
];

async function fetchUsers() {
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

function openAddDialog() {
    newUser.value = {
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        password: "",
        password_confirm: "",
    };
    editMode.value = false;
    editingUserId.value = null;
    fieldErrors.value = {};
    addError.value = "";
    addDialog.value = true;
}

function openEditDialog(user) {
    newUser.value = {
        username: user.username,
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name,
        password: "",
        password_confirm: "",
    };
    editMode.value = true;
    editingUserId.value = user.id;
    fieldErrors.value = {};
    addError.value = "";
    addDialog.value = true;
}

async function handleSaveUser() {
    fieldErrors.value = {};
    saving.value = true;
    addError.value = "";
    try {
        if (editMode.value) {
            const payload = { ...newUser.value };
            if (!payload.password) {
                delete payload.password;
                delete payload.password_confirm;
            }
            await api.patch(`/users/${editingUserId.value}/`, payload);
        } else {
            await api.post("/users/", newUser.value);
        }
        addDialog.value = false;
        fetchUsers();
    } catch (error) {
        if (error.response && error.response.data) {
            fieldErrors.value = error.response.data;
        } else {
            addError.value = "İşlem sırasında bir hata oluştu.";
        }
    } finally {
        saving.value = false;
    }
}

function openDeleteDialog(user) {
    userToDelete.value = user;
    deleteDialog.value = true;
}

async function handleDeleteUser() {
    deleting.value = true;
    try {
        await api.delete(`/users/${userToDelete.value.id}/`);
        deleteDialog.value = false;
        fetchUsers();
    } catch (error) {
        console.error("Kullanıcı silinemedi:", error);
    } finally {
        deleting.value = false;
    }
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
            <v-btn color="primary" @click="openAddDialog">Ekle</v-btn>
        </div>

        <v-data-table :headers="headers" :items="users" :loading="loading">
            <template v-slot:item.actions="{ item }">
                <v-btn
                    icon="mdi-pencil"
                    size="small"
                    variant="text"
                    @click="openEditDialog(item)"
                />
                <v-btn
                    icon="mdi-delete"
                    size="small"
                    color="error"
                    variant="text"
                    @click="openDeleteDialog(item)"
                />
            </template>
        </v-data-table>
        <v-dialog v-model="addDialog" max-width="700">
            <v-card>
                <v-card-title>{{
                    editMode ? "Kullanıcı Düzenle" : "Kullanıcı Ekle"
                }}</v-card-title>
                <v-card-text>
                    <v-form ref="formRef">
                        <v-text-field
                            v-model="newUser.username"
                            label="Kullanıcı Adı"
                            required
                            :error-messages="fieldErrors.username"
                        />

                        <v-text-field
                            v-model="newUser.email"
                            label="Email"
                            required
                            :error-messages="fieldErrors.email"
                        />

                        <v-text-field
                            v-model="newUser.first_name"
                            label="Ad"
                            required
                            :error-messages="fieldErrors.first_name"
                        />

                        <v-text-field
                            v-model="newUser.last_name"
                            label="Soyad"
                            required
                            :error-messages="fieldErrors.last_name"
                        />

                        <v-text-field
                            v-model="newUser.password"
                            label="Şifre"
                            type="password"
                            :required="!editMode"
                            :hint="
                                editMode
                                    ? 'Değiştirmek istemiyorsan boş bırak'
                                    : ''
                            "
                            persistent-hint
                            :error-messages="fieldErrors.password"
                        />

                        <v-text-field
                            v-model="newUser.password_confirm"
                            label="Şifre Tekrar"
                            type="password"
                            :required="!editMode"
                            :error-messages="fieldErrors.password_confirm"
                        />

                        <v-alert
                            v-if="addError"
                            type="error"
                            density="compact"
                            class="mt-2"
                        >
                            {{ addError }}
                        </v-alert>
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer />
                    <v-btn @click="addDialog = false">İptal</v-btn>
                    <v-btn
                        color="primary"
                        :loading="saving"
                        @click="handleSaveUser"
                        >Kaydet</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="deleteDialog" max-width="400">
            <v-card>
                <v-card-title>Kullanıcıyı Sil</v-card-title>
                <v-card-text>
                    <strong>{{ userToDelete?.username }}</strong>
                    kullanıcısını silmek istediğinize emin misiniz?
                </v-card-text>
                <v-card-actions>
                    <v-spacer />
                    <v-btn @click="deleteDialog = false">Hayır</v-btn>
                    <v-btn
                        color="error"
                        :loading="deleting"
                        @click="handleDeleteUser"
                        >Evet</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api";
import { useAuthStore } from "../stores/auth";

const tasks = ref([]);
const loading = ref(false);
const authStore = useAuthStore();
const addDialog = ref(false);
const saving = ref(false);
const fieldErrors = ref({});
const users = ref([]);
const newTask = ref({
    task_name: "",
    task_description: "",
    state: "TODO",
    user: null,
});

const deleteDialog = ref(false);
const taskToDelete = ref(null);
const deleting = ref(false);

function openDeleteDialog(task) {
    taskToDelete.value = task;
    deleteDialog.value = true;
}

async function handleDeleteTask() {
    deleting.value = true;
    try {
        await api.delete(`/tasks/${taskToDelete.value.id}/`);
        deleteDialog.value = false;
        fetchTasks();
    } catch (error) {
        console.error("Görev silinemedi:", error);
    } finally {
        deleting.value = false;
    }
}

const headers = [
    { title: "Başlık", key: "task_name" },
    { title: "Açıklama", key: "task_description" },
    { title: "Durum", key: "state" },
    { title: "Kullanıcı", key: "assigned_username" },
    { title: "Actions", key: "actions", sortable: false },
];

function stateColor(state) {
    if (state === "TODO") return "amber";
    if (state === "IN_PROGRESS") return "blue";
    if (state === "DONE") return "green";
    return "grey";
}

async function fetchTasks() {
    loading.value = true;
    try {
        const response = await api.get("/tasks/");
        tasks.value = response.data;
    } catch (error) {
        console.error("Görevler alınamadı:", error);
    } finally {
        loading.value = false;
    }
}

async function fetchUsersForSelect() {
    if (!authStore.isAdmin) return;
    try {
        const response = await api.get("/users/");
        users.value = response.data;
    } catch (error) {
        console.error("Kullanıcılar alınamadı:", error);
    }
}

function openAddDialog() {
    newTask.value = {
        task_name: "",
        task_description: "",
        state: "TODO",
        user: null,
    };
    fieldErrors.value = {};
    addDialog.value = true;
}

async function handleAddTask() {
    saving.value = true;
    fieldErrors.value = {};
    try {
        await api.post("/tasks/", newTask.value);
        addDialog.value = false;
        fetchTasks();
    } catch (error) {
        if (error.response && error.response.data) {
            fieldErrors.value = error.response.data;
        }
    } finally {
        saving.value = false;
    }
}
onMounted(() => {
    fetchTasks();
    fetchUsersForSelect();
});
</script>

<template>
    <v-container>
        <h1 class="mb-4">Görevler</h1>
        <div class="d-flex justify-end mb-4">
            <v-btn color="primary" @click="openAddDialog">Ekle</v-btn>
        </div>

        <v-data-table :headers="headers" :items="tasks" :loading="loading">
            <template v-slot:item.assigned_username="{ item }">
                {{ item.assigned_username || "Atanmamış" }}
            </template>
            <template v-slot:item.state="{ item }">
                <v-chip :color="stateColor(item.state)" size="small">
                    {{ item.state }}
                </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn
                    v-if="
                        authStore.isAdmin ||
                        item.user === Number(authStore.userId)
                    "
                    icon="mdi-delete"
                    size="small"
                    color="error"
                    variant="text"
                    @click="openDeleteDialog(item)"
                />
            </template>
        </v-data-table>
        <v-dialog v-model="addDialog" max-width="600">
            <v-card>
                <v-card-title>Görev Ekle</v-card-title>
                <v-card-text>
                    <v-text-field
                        v-model="newTask.task_name"
                        label="Başlık"
                        required
                        :error-messages="fieldErrors.task_name"
                    />
                    <v-textarea
                        v-model="newTask.task_description"
                        label="Açıklama"
                        :error-messages="fieldErrors.task_description"
                    />
                    <v-select
                        v-if="authStore.isAdmin"
                        v-model="newTask.user"
                        :items="users"
                        item-title="username"
                        item-value="id"
                        label="Kime atansın"
                        required
                        :error-messages="fieldErrors.user"
                    />
                </v-card-text>
                <v-card-actions>
                    <v-spacer />
                    <v-btn @click="addDialog = false">İptal</v-btn>
                    <v-btn
                        color="primary"
                        :loading="saving"
                        @click="handleAddTask"
                        >Kaydet</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="deleteDialog" max-width="400">
            <v-card>
                <v-card-title>Görevi Sil</v-card-title>
                <v-card-text>
                    <strong>{{ taskToDelete?.task_name }}</strong> görevini
                    silmek istediğinize emin misiniz?
                </v-card-text>
                <v-card-actions>
                    <v-spacer />
                    <v-btn @click="deleteDialog = false">Hayır</v-btn>
                    <v-btn
                        color="error"
                        :loading="deleting"
                        @click="handleDeleteTask"
                        >Evet</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

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

const detailDialog = ref(false);
const selectedTask = ref(null);
const editTask = ref({});
const savingEdit = ref(false);
const comments = ref([]);
const newComment = ref("");
const editingCommentId = ref(null);
const editingCommentContent = ref("");

// Yorum silme penceresi için gerekli değişkenler
const deleteCommentDialog = ref(false);
const commentToDeleteId = ref(null);

// Çöp kutusuna tıklanınca pencereyi açan fonksiyon
const openDeleteCommentDialog = (id) => {
    commentToDeleteId.value = id;
    deleteCommentDialog.value = true;
};

// Penceredeki "Evet, Sil" butonuna tıklanınca çalışacak fonksiyon
const confirmDeleteComment = async () => {
    if (commentToDeleteId.value) {

        // Yorum silme fonksiyonu ID ile çağırıyoruz
        await deleteComment(commentToDeleteId.value);
        // İşlem bitince popup kapat
        deleteCommentDialog.value = false;
    }
};

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

async function openDetail(task) {
    selectedTask.value = task;
    editTask.value = { ...task };
    detailDialog.value = true;
    await fetchComments(task.id);
}

async function fetchComments(taskId) {
    const response = await api.get(`/comments/?task=${taskId}`);
    comments.value = response.data;
}

async function handleUpdateTask() {
    savingEdit.value = true;
    try {
        await api.patch(`/tasks/${selectedTask.value.id}/`, editTask.value);
        detailDialog.value = false;
        fetchTasks();
    } catch (error) {
        console.error("Görev güncellenemedi:", error);
    } finally {
        savingEdit.value = false;
    }
}

async function addComment() {
    if (!newComment.value.trim()) return;
    await api.post("/comments/", {
        task: selectedTask.value.id,
        content: newComment.value,
    });
    newComment.value = "";
    fetchComments(selectedTask.value.id);
}

function startEditComment(c) {
    editingCommentId.value = c.id;
    editingCommentContent.value = c.content;
}

async function saveCommentEdit(c) {
    await api.patch(`/comments/${c.id}/`, {
        content: editingCommentContent.value,
    });
    editingCommentId.value = null;
    fetchComments(selectedTask.value.id);
}

async function deleteComment(id) {
    await api.delete(`/comments/${id}/`);
    fetchComments(selectedTask.value.id);
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
                    icon="mdi-pencil"
                    size="small"
                    variant="text"
                    @click="openDetail(item)"
                />
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

        <v-dialog v-model="addDialog" max-width="1100">
            <v-card>
                <v-card-title>Görev Ekle</v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col cols="12" md="6">
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
                        </v-col>
                    </v-row>
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
                    Bu görevi silmek istediğinize emin misiniz? Bu işlem geri
                    alınamaz.
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


        <!-- YAN YANA DETAY VE YORUM PENCERESİ -->

        <v-dialog v-model="detailDialog" max-width="1000">
            <v-card>
                <v-card-title class="text-h5 pb-3">{{
                    selectedTask?.task_name
                }}</v-card-title>
                <v-card-text>
                    <v-row>
                        <v-col cols="12" md="6" class="pr-md-4">
                            <h3 class="mb-4">Detaylar</h3>

                            <v-text-field
                                v-model="editTask.task_name"
                                label="Başlık"
                                variant="outlined"
                            />
                            <v-textarea
                                v-model="editTask.task_description"
                                label="Açıklama"
                                variant="outlined"
                                rows="4"
                            />
                            <v-select
                                v-model="editTask.state"
                                :items="['TODO', 'IN_PROGRESS', 'DONE']"
                                label="Durum"
                                variant="outlined"
                            />
                            <v-select
                                v-if="authStore.isAdmin"
                                v-model="editTask.user"
                                :items="users"
                                item-title="username"
                                item-value="id"
                                label="Kime atansın"
                                variant="outlined"
                            />
                            <v-btn
                                color="primary"
                                :loading="savingEdit"
                                @click="handleUpdateTask"
                                block
                                >Güncelle</v-btn
                            >
                        </v-col>

                        <v-col
                            cols="12"
                            md="6"
                            class="pl-md-4"
                            style="border-left: 1px solid #eee"
                        >
                            <h3 class="mb-4">Yorumlar</h3>

                            <v-textarea
                                v-model="newComment"
                                label="Bir yorum yaz..."
                                variant="outlined"
                                rows="2"
                            />
                            <v-btn
                                color="primary"
                                @click="addComment"
                                class="mb-4"
                                variant="tonal"
                                >Gönder</v-btn
                            >

                            <v-divider class="mb-4" />

                            <v-list class="bg-transparent">
                                <v-list-item
                                    v-for="c in comments"
                                    :key="c.id"
                                    class="px-0 mb-2"
                                >
                                    <template v-if="editingCommentId === c.id">
                                        <v-textarea
                                            v-model="editingCommentContent"
                                            rows="2"
                                            variant="outlined"
                                        />
                                        <div class="d-flex gap-2 mt-2">
                                            <v-btn
                                                size="small"
                                                color="success"
                                                @click="saveCommentEdit(c)"
                                                >Kaydet</v-btn
                                            >
                                            <v-btn
                                                size="small"
                                                variant="text"
                                                @click="editingCommentId = null"
                                                >İptal</v-btn
                                            >
                                        </div>
                                    </template>

                                    <template v-else>
                                        <v-list-item-title
                                            class="font-weight-bold text-primary"
                                        >
                                            {{ c.author_username }}
                                        </v-list-item-title>
                                        <v-list-item-subtitle
                                            class="mt-1"
                                            style="
                                                white-space: pre-line;
                                                opacity: 0.9;
                                            "
                                        >
                                            {{ c.content }}
                                        </v-list-item-subtitle>
                                    </template>

                                    <template
                                        v-slot:append
                                        v-if="
                                            editingCommentId !== c.id &&
                                            (authStore.isAdmin ||
                                                c.author ===
                                                    Number(authStore.userId))
                                        "
                                    >
                                        <v-btn
                                            icon="mdi-pencil"
                                            size="small"
                                            variant="text"
                                            color="grey-darken-1"
                                            @click="startEditComment(c)"
                                        />
                                        <v-btn
                                            icon="mdi-delete"
                                            size="small"
                                            variant="text"
                                            color="error"
                                            @click="
                                                openDeleteCommentDialog(c.id)
                                            "
                                        />
                                    </template>
                                </v-list-item>
                            </v-list>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-dialog>
        <v-dialog v-model="deleteCommentDialog" max-width="400">
            <v-card>
                <v-card-title>Yorumu Sil</v-card-title>
                <v-card-text>
                    Bu yorumu silmek istediğinize emin misiniz? Bu işlem geri
                    alınamaz.
                </v-card-text>
                <v-card-actions>
                    <v-spacer />
                    <v-btn @click="deleteCommentDialog = false">Hayır</v-btn>
                    <v-btn color="error" @click="confirmDeleteComment"
                        >Evet</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

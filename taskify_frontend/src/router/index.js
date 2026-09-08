import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

const routes = [
    {
        path: "/login",
        name: "Login",
        component: () => import("../views/LoginView.vue"),
    },
    {
        path: "/",
        name: "Home",
        component: () => import("../views/HomeView.vue"),
    },
    {
        path: "/users",
        name: "Users",
        component: () => import("../views/UsersView.vue"),
    },
    {
        path: "/tasks",
        name: "Tasks",
        component: () => import("../views/TasksView.vue"),
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    //her sayfa geçişinde beforeEach çalışır - login kontrolü için
    const authStore = useAuthStore();
    if (to.name !== "Login" && !authStore.isLoggedIn) {
        next({ name: "Login" }); //login değilse - giriş yapmamışsa logine yönlendir
    } else {
        next();
    }
});

export default router;

import { createRouter, createWebHistory } from "vue-router";

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

export default router;

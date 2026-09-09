import axios from "axios";
import { useAuthStore } from "./stores/auth";

const api = axios.create({
    baseURL: "/api", // her istekte /api/login/ yazmaya gerek kalmayacak login yazıcaz api otomatik eklenicek
});

api.interceptors.request.use((config) => {
    //her istekten önce çalışacak fonksiyon
    const authStore = useAuthStore();
    if (authStore.token) {
        //autstore'da token varsa header'a token eklenir
        config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
});

export default api;

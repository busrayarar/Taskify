import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        //storeun tuttuğu veriler (token, username, admin mi?)
        token: localStorage.getItem("access_token") || null,
        username: localStorage.getItem("username") || null,
        userId: localStorage.getItem("user_id") || null,
        isAdmin: localStorage.getItem("is_admin") === "true",
    }), //sayfa yenilenince kaybolmasın local storage - tarayıcının kalıcı depolama alanı

    getters: {
        isLoggedIn: (state) => !!state.token, //token var mı yok mu true/false
    },

    actions: {
        //login başarılıysa çalışan fonk hem store hem state güncellenir - kalıcılık için
        setAuth(token, username, userId, isAdmin) {
            this.token = token;
            this.username = username;
            this.isAdmin = isAdmin;
            this.userId = userId;

            localStorage.setItem("access_token", token);
            localStorage.setItem("username", username);
            localStorage.setItem("is_admin", isAdmin);
            localStorage.setItem("user_id", userId);
        },

        logout() {
            //çıkış yapılınca her şey temizlenir
            this.token = null;
            this.username = null;
            this.isAdmin = false;
            this.userId = null;

            localStorage.removeItem("access_token");
            localStorage.removeItem("username");
            localStorage.removeItem("is_admin");
            localStorage.removeItem("user_id");
        },
    },
});

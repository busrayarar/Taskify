import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        //storeun tuttuğu veriler (token, username, admin mi?)
        token: localStorage.getItem("access_token") || null,
        username: localStorage.getItem("username") || null,
        isAdmin: localStorage.getItem("is_admin") === "true",
    }), //sayfa yenilenince kaybolmasın local storage - tarayıcının kalıcı depolama alanı

    getters: {
        isLoggedIn: (state) => !!state.token, //token var mı yok mu true/false
    },

    actions: {
        //login başarılıysa çalışan fonk hem store hem state güncellenir - kalıcılık için
        setAuth(token, username, isAdmin) {
            this.token = token;
            this.username = username;
            this.isAdmin = isAdmin;

            localStorage.setItem("access_token", token);
            localStorage.setItem("username", username);
            localStorage.setItem("is_admin", isAdmin);
        },

        logout() {
            //çıkış yapılınca her şey temizlenir
            this.token = null;
            this.username = null;
            this.isAdmin = false;

            localStorage.removeItem("access_token");
            localStorage.removeItem("username");
            localStorage.removeItem("is_admin");
        },
    },
});

import "@mdi/font/css/materialdesignicons.css"; //mdı stil dosyası
import "vuetify/styles"; //vuetifyın css dosyası
import { createVuetify } from "vuetify";

export default createVuetify({
    icons: {
        defaultSet: "mdi",
    },
    theme: {
        defaultTheme: "light",
    },
});

import "@mdi/font/css/materialdesignicons.css"; //mdı stil dosyası
import "vuetify/styles"; //vuetifyın css dosyası
import { createVuetify } from "vuetify";

export default createVuetify({
    theme: {
        defaultTheme: "light",
        themes: {
            light: {
                colors: {
                    background: "#FFFFFF",
                    surface: "#F7F7F5",
                    "notion-blue": "#E1EDF8",
                    "notion-yellow": "#FDF3D9",
                    "notion-green": "#DDEFE2",
                    "notion-text": "#37352F",
                },
            },
            dark: {
                dark: true,
                colors: {
                    background: "#191919",
                    surface: "#252525",
                    "notion-blue": "#1F2937",
                    "notion-yellow": "#3A331F",
                    "notion-green": "#1F3327",
                    "notion-text": "#E9E9E7",
                },
            },
        },
    },
});

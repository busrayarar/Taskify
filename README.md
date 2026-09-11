# Taskify - Görev Takip ve İşbirliği Uygulaması

Kullanıcıların görevlerini oluşturup takip edebildiği, yorum yapabildiği ve rol bazlı (admin/kullanıcı) yetkilendirmeyle çalışan bir görev yönetim platformu.

## Özellikler

### Güvenlik ve Kimlik Doğrulama

- JWT Tabanlı Oturum Yönetimi: Güvenli login sistemi ve token tabanlı kimlik doğrulama.
- Rol Bazlı Erişim Kontrolü: Admin ve normal kullanıcılar için tamamen izole edilmiş sayfa görünümleri ve yetki sınırlandırmaları.

### Kullanıcı ve Görev Yönetimi

- Kullanıcı Yönetimi: Sisteme kayıtlı kullanıcıları listeleme, backend bağlantılı detaylı arama/filtreleme, yeni kullanıcı ekleme, düzenleme ve silme.
- Görev (Task) Modülü: Yeni görev oluşturma, kullanıcılara atama yapma, düzenleme, silme ve durum (TODO, IN_PROGRESS, DONE) güncelleme.
- İnteraktif İşbirliği: Görevler üzerinde iletişim kurabilmek için yorum ekleme, düzenleme ve onaylı silme sistemi.

### Arayüz (UI/UX)

- Dashboard Panelleri: Anasayfada durum bazlı istatistik panelleri (Adminler için tüm sistemin, normal kullanıcılar için yalnızca kendilerine atanan görevlerin özeti).
- Modern Tasarım: Açık/koyu (Light/Dark) tema desteğine sahip, Vuetify 3 ile geliştirilmiş arayüz.

### Altyapı ve Mimari

- Konteyner Mimarisi: Docker Compose kullanılarak birbirlerinden izole edilmiş multi-container (Django, PostgreSQL, Vue 3, Nginx) çalışma ortamı.
- Nginx Reverse Proxy: İstemciden gelen tüm isteklerin Nginx üzerinden geçerek ilgili konteynerlara güvenli yönlendirilmesi.
- Otomatik Seeding: database_init scripti sayesinde, sistem ayağa kalktığı anda varsayılan admin hesabının ve örnek verilerin otomatik olarak oluşturulması.

## Proje Yapısı

```
Taskify/
├── taskify_frontend/         # Vue 3 + Vuetify 3 Frontend Uygulaması
│   ├── src/
│   │   ├── plugins/          # Vuetify (vuetify.js) ve eklenti ayarları
│   │   ├── router/           # Vue Router (Sayfa ve yetki yönlendirmeleri)
│   │   ├── stores/           # State Management (auth.js ile token/kullanıcı yönetimi)
│   │   ├── views/            # Sayfalar (HomeView, LoginView, TasksView, UsersView)
│   │   ├── api.js            # Backend ile API haberleşme ayarları (Axios/Fetch)
│   │   ├── App.vue           # Ana Vue Bileşeni ve Layout
│   │   └── main.js           # Uygulama Giriş Noktası
│   ├── Dockerfile            # Frontend konteyner yapılandırması
│   ├── package.json          # Frontend bağımlılıkları
│   └── vite.config.js        # Vite ve sunucu yapılandırması
│
├── taskify_backend/          # Django REST Framework API
│   ├── core/                 # Ana Django Proje Ayarları (settings.py, urls.py vb.)
│   ├── tasks/                # İş mantığı, Görev ve Kullanıcı modülü
│   │   ├── models.py         # Veritabanı Tablo Modelleri
│   │   ├── serializers.py    # Frontend ile iletişim için JSON dönüşümleri
│   │   ├── urls.py           # API Uç Noktaları (Endpoints)
│   │   └── views.py          # Yetkilendirme ve CRUD Operasyonları
│   ├── Dockerfile            # Backend konteyner yapılandırması
│   ├── manage.py             # Django yönetim dosyası
│   └── requirements.txt      # Python kütüphane bağımlılıkları
│
├── .env                      # Ortam değişkenleri (Veritabanı şifreleri, portlar vb.)
├── docker-compose.yml        # Tüm sistemi izole konteynerlerde ayağa kaldıran dosya
└── nginx.conf                # İstemci trafiklerini backend/frontend'e dağıtan Nginx ayarı
```

## Kullanılan Teknolojiler

**Frontend**

- **Vue 3:** Modern, reaktif ve performanslı kullanıcı arayüzü kütüphanesi.
- **Vuetify 3:** Material Design standartlarına uygun, zengin UI bileşen kütüphanesi.
- **Vue Router:** Sayfa içi yönlendirmeler ve yetki tabanlı sayfa koruması.
- **Vuex / Pinia:** Merkezi durum yönetimi (State Management) ve JWT token tutma.
- **Vite:** Yeni nesil, hızlı frontend derleme ve geliştirme aracı.

**Backend**

- **Python:** Temel geliştirme dili.
- **Django:** Güvenilir ve ölçeklenebilir backend web framework'ü.
- **Django REST Framework (DRF):** Modern RESTful API altyapısı ve JSON serileştirme.
- **JWT (JSON Web Tokens):** Güvenli, stateless kimlik doğrulama mimarisi.

**Veritabanı**

- **PostgreSQL:** Güçlü, açık kaynaklı ve ilişkisel veritabanı yönetim sistemi.

**Altyapı & Dağıtım**

- **Docker:** Uygulama izolasyonu ve konteynerizasyon.
- **Docker Compose:** Çoklu konteyner (Multi-container) yönetimi ve dağıtımı.
- **Nginx:** Reverse proxy, port yönlendirme ve istemci isteklerinin yönetimi.

## Kurulum ve Çalıştırma (Installation & Setup)

Bu proje, tüm bağımlılıkları ve servisleri izole bir şekilde çalıştırabilmek için **Docker** ve **Docker Compose** kullanılarak yapılandırılmıştır. Uygulamayı bilgisayarınızda çalıştırmak için aşağıdaki adımları izlemeniz yeterlidir.

### Ön Koşullar (Prerequisites)

Bilgisayarınızda aşağıdaki araçların kurulu olduğundan emin olun:

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Kurulum

**1. Projeyi Klonlayın**

```bash
git clone https://github.com/busrayarar/taskify.git
cd taskify
```

**2. Çevresel Değişkenleri (Environment Variables) Ayarlayın**
Proje ana dizininde bulunan `.env.example` dosyasının adını `.env` olarak değiştirin veya yeni bir `.env` dosyası oluşturup gerekli veritabanı/sistem değişkenlerini tanımlayın:

```bash
DB_NAME=taskify_db
DB_USER=taskify_user
DB_PASSWORD=taskify_password
DJANGO_ADMIN_PASSWORD=your_admin_password_here
```

**3. Konteynerleri Ayağa Kaldırın**
Aşağıdaki tek satırlık komut ile Frontend, Backend, PostgreSQL ve Nginx servislerini derleyip başlatabilirsiniz:

```bash
docker compose up -d --build
```

**4. Sisteme Erişin**
Konteynerler başarıyla ayağa kalktıktan sonra, Nginx yönlendirmeleri sayesinde uygulamaya tarayıcınızdan erişebilirsiniz:

- Frontend: `http://localhost`
- Backend: `http://localhost/api`

#### Not:

Proje içerisindeki `database_init` script'i sayesinde veritabanı tabloları, varsayılan admin hesabı ve örnek veriler sistem ilk kez ayağa kalktığında otomatik olarak oluşturulur. Ekstra bir `migrate` komutu çalıştırmanıza gerek yoktur.

**5. Konteynerleri Durdurma**

- Servisleri durdurmak için:

```bash
docker compose down
```

- Servisleri durdurup veritabanı verilerini (volume) de tamamen silmek için:

```bash
docker compose down -v
```

### Uyarı:

`-v` parametresi veritabanı volume'ünü de sileceği için tüm veriler (kullanıcılar, task'lar, yorumlar vb.) kalıcı olarak kaybolur. Sistemi tekrar `docker compose up -d --build` ile ayağa kaldırdığınızda `database_init` script'i sayesinde veritabanı sıfırdan ve örnek verilerle yeniden oluşturulur.

## Test Hesapları (Demo Credentials)

Sistemi test edebilmeniz için başlangıçta aşağıdaki varsayılan hesap otomatik olarak oluşturulmaktadır:

**Admin Hesabı (Tam Yetkili):**

- **Kullanıcı Adı:** `admin`
- **Şifre:** `A114474.min`

> **Önemli:** Bu şifre yalnızca yerel geliştirme ortamı içindir. Uygulamayı canlı sunucuya taşıdığınızda bu varsayılan şifreyi değiştirin.

## API Endpoints

### Comments

| Method | Endpoint              |
| ------ | --------------------- |
| GET    | `/api/comments/`      |
| POST   | `/api/comments/`      |
| GET    | `/api/comments/{id}/` |
| PUT    | `/api/comments/{id}/` |
| PATCH  | `/api/comments/{id}/` |
| DELETE | `/api/comments/{id}/` |

### Login

| Method | Endpoint      |
| ------ | ------------- |
| POST   | `/api/login/` |

### Tasks

| Method | Endpoint            |
| ------ | ------------------- |
| GET    | `/api/tasks/`       |
| POST   | `/api/tasks/`       |
| GET    | `/api/tasks/{id}/`  |
| PUT    | `/api/tasks/{id}/`  |
| PATCH  | `/api/tasks/{id}/`  |
| DELETE | `/api/tasks/{id}/`  |
| GET    | `/api/tasks/stats/` |

### Token

| Method | Endpoint              |
| ------ | --------------------- |
| POST   | `/api/token/refresh/` |

### Users

| Method | Endpoint           |
| ------ | ------------------ |
| GET    | `/api/users/`      |
| POST   | `/api/users/`      |
| GET    | `/api/users/{id}/` |
| PUT    | `/api/users/{id}/` |
| PATCH  | `/api/users/{id}/` |
| DELETE | `/api/users/{id}/` |

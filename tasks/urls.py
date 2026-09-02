from django.urls import path, include
from rest_framework.routers import DefaultRouter #router ile viewsetleri bağlamak için
from . import views 

# router've viewsetler
router = DefaultRouter() #router başlat 
router.register(r'users', views.UserViewSet, basename='user') # sınıfları routera kayde - urlde görünücek ismi yaz - hangi sınıfa gideceğini belirt - 
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'comments', views.CommentViewSet, basename='comment')
# router arka plnada otomatik olarak get/listele - post/oluştur - get/detay - put/güncelle - delete/sil rotalarını oluşturuyor. 

urlpatterns = [
    path('', include(router.urls)), # içine router.urls ekleyerek routerın oluşturduğu rotaları dahil ediyoruz.
]
from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User
from .models import Task, Comment
from .serializers import UserSerializer, TaskSerializer, CommentSerializer
from rest_framework import filters, viewsets, permissions

# sadece taskı açan user veya admin düzenleyebilir - user silemez 
class IsOwnerAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): #istek atan kişi kim - hangi viewset - o an işlem yapılmak istenen obje 
        if request.method in permissions.SAFE_METHODS: # değişmeten veriler readonly olanlara istek dönerse direkt true döner
            return True
        return bool(request.user and (request.user.is_staff or obj.user == request.user)) # istek readonly değilse değişebilirse istek atan user var mı bu user admin mi veya user task sahibi mi bu ikisinden biriyse true döner

# sadece admin görebilir
class UserViewSet(viewsets.ModelViewSet): #model ve serializer alıp crud rotalarını hazırlıyoruz
    queryset = User.objects.all()  #herkes üstünde çalışıcak
    serializer_class = UserSerializer # jsona nası dönücek
    permission_classes = [IsAdminUser]  # sadece admin görebilir
    filter_backends = [filters.SearchFilter] # arama motorunu aktif et
    search_fields = ['username', 'email', 'first_name', 'last_name'] #sadece bu fieldlerde arama yapabiliriz

# herkes görebilir 
class TaskViewSet(viewsets.ModelViewSet): 
    queryset = Task.objects.all() #her taskta çalışıcak
    serializer_class = TaskSerializer #jsona nası dönücek
    permission_classes = [IsAuthenticated, IsOwnerAdminOrReadOnly] #giriş yapmış mı ve taskın userı mı ya da admin mi 

# sadece kendi tasklarını görebilir ve filtreleme yapabilir
    def get_queryset(self):
        queryset = super().get_queryset()
        assigned_to_me = self.request.query_params.get('assigned_to_me')
        if assigned_to_me == 'true':
            queryset = queryset.filter(user=self.request.user)
        return queryset

# admin değilse görev onun adminse serializersten gelen?
    def perform_create(self, serializer): # post isteğinden önce araya girmemizi sağlıyor
        if not self.request.user.is_staff:  #kullanıcı admin değilse taskı atan user sahibi olur adminse serializerden gelen user taskın sahibi olur
            serializer.save(user=self.request.user) 
        else:
            serializer.save()

# yorumlar herkes görebilir
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all() # tüm yorumlar üzerinde çalışır
    serializer_class = CommentSerializer 
    permission_classes = [IsAuthenticated, IsOwnerAdminOrReadOnly] # girirş yapmış mı ve yorumun userı mı ya da admin mi

# yorumu atan user sahibi 
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
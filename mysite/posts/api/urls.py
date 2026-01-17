# blog/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .. import views  # две точки значит "из родительской папки"

# СОЗДАЁМ РОУТЕР - он автоматически создаст адреса
router = DefaultRouter()

# РЕГИСТРИРУЕМ ViewSet для статей
# 'posts' - будет в URL: /api/posts/
# views.PostViewSet - класс который обрабатывает запросы
router.register(r'posts', views.PostViewSet)

# ВСЕ АДРЕСА которые создал роутер
urlpatterns = [
    path('', include(router.urls)),
]
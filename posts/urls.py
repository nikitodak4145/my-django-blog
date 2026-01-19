"""
posts/urls.py
Здесь мы говорим: "Какие URL ведут к каким страницам в приложении posts?"
"""

from django.urls import path
from . import views  # Импортируем наши views (обработчики)

# Список маршрутов



urlpatterns = [
    path('', views.post_list, name='post_list'),  # главная
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # страница статьи
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('analytics/', views.analytics, name='analytics'), 
    path('api/post/<int:post_id>/increment-views/', views.api_increment_views, name='api_increment_views'), # ← новая строка
]
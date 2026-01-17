"""
posts/urls.py
Здесь мы говорим: "Какие URL ведут к каким страницам в приложении posts?"
"""

from django.urls import path
from . import views  # Импортируем наши views (обработчики)

# Список маршрутов
urlpatterns = [
    # Маршрут для списка статей
    # '' = относительный путь (будет подключен к главным URL)
    # Но мы создадим его в следующем файле
    path('', views.post_list, name='post_list'),
]



urlpatterns = [
    path('', views.post_list, name='post_list'),  # главная
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # страница статьи
]
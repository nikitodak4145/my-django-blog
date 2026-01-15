"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
blog_project/urls.py
Главный файл маршрутов всего проекта
Здесь подключаем маршруты из приложений
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Админ-панель (будет доступна по /admin/)
    path('admin/', admin.site.urls),
    
    # Подключаем маршруты из приложения posts
    # 'posts/' = префикс (все маршруты из posts будут начинаться с /posts/)
    # include('posts.urls') = "Включи все маршруты из posts/urls.py"
    path('posts/', include('posts.urls')),
    
    # Дополнительно: главная страница тоже ведет к списку статей
    path('', include('posts.urls')),  # Теперь сайт.ru/ тоже покажет статьи
]
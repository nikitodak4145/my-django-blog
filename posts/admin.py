from django.contrib import admin

# Register your models here.


from .models import Post  # Импортируем нашу модель

@admin.register(Post)  # "Зарегистрируй модель Post в админке"
class PostAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения статей в админке
    """
    
    # Какие поля показывать в списке статей
    list_display = ['title', 'created_at']
    
    # По каким полям можно искать
    search_fields = ['title', 'content']
    
    # Фильтры справа (по дате)
    list_filter = ['created_at']
    
    # Поля только для чтения
    readonly_fields = ['created_at']
    
    # Как группировать поля при редактировании
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content')
        }),
        ('Дата', {
            'fields': ('created_at',),
            'classes': ('collapse',)  # Можно свернуть/развернуть
        }),
    )

    # posts/admin.py

from .models import Comment

# 2. РЕГИСТРИРУЕМ В АДМИНКЕ С НАСТРОЙКАМИ
# @admin.register = декоратор = "оберни функцию в дополнительную логику"
# Comment = модель которую регистрируем
# admin.site.register(Comment) ← старый способ (просто регистрация)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 3. КАК ОТОБРАЖАТЬ СПИСОК КОММЕНТАРИЕВ
    # list_display = какие поля показывать в таблице
    list_display = ('author', 'post', 'created_at')
    
    # 4. ФИЛЬТРЫ СБОКУ (ДЛЯ БЫСТРОГО ПОИСКА)
    # list_filter = по каким полям можно фильтровать
    # created_at = фильтр по дате (сегодня, неделя, месяц)
    # post = фильтр по статье
    list_filter = ('created_at', 'post')
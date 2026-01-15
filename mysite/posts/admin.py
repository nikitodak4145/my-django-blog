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
from django.db import models
from django.utils import timezone

class Post(models.Model):
    """
    Класс Post = одна таблица в базе данных
    Каждое поле = столбец в таблице
    """
    
    # Поле "Заголовок" - максимум 200 символов
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок статьи"  # Красивое имя для админки
    )
    
    # Поле "Текст статьи" - может быть очень длинным
    content = models.TextField(
        verbose_name="Текст статьи"
    )
    
    # Поле "Дата создания" - автоматически ставит текущее время
    created_at = models.DateTimeField(
        default=timezone.now,  # Автоматически = сейчас
        verbose_name="Дата создания"
    )
    
    def __str__(self):
        """
        Как будет отображаться статья в админке
        Например: "Моя первая статья"
        """
        return self.title
    
    class Meta:
        """
        Дополнительные настройки модели
        """
        ordering = ['-created_at']  # Сортировка: новые статьи сверху
        verbose_name = "Статья"  # Название в единственном числе
        verbose_name_plural = "Статьи"  # Название во множественном числе

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100, default='Аноним')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Комментарий от {self.author} к "{self.post.title}"'       
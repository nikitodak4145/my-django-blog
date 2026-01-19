from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)  # ← ПОЛЕ ПРОСМОТРОВ!
    
    def __str__(self):
        return self.title
    

    
    def increment_views(self):
        """Увеличивает просмотры и возвращает новое значение"""
        self.views += 1
        self.save(update_fields=['views'])
        return self.views
    
    class Meta:
        ordering = ['-created_at']  # новые статьи сверху
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100, default='Аноним')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # УБРАТЬ views из Comment! Просмотры только у статей
    # views = models.PositiveIntegerField(default=0)  ← УДАЛИ ЭТУ СТРОКУ!
    
    def __str__(self):
        return f'Комментарий от {self.author} к "{self.post.title}"'
    
    class Meta:
        ordering = ['created_at']  # старые комментарии сверху
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
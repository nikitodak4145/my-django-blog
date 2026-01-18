# posts/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    # Meta класс = настройки формы
    class Meta:
        model = Comment  # Связываем с моделью Comment
        fields = ['author', 'text']  # Какие поля показывать
        # Поле post НЕ показываем - его установим автоматически!
        
    # Улучшаем поля
    author = forms.CharField(
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    
    text = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Оставьте ваш комментарий...',
            'rows': 3
        })
    )
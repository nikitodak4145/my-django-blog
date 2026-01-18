# posts/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Post, Comment
from rest_framework import viewsets
from .serializers import PostSerializer
from .forms import CommentForm  
from django.utils import timezone
def post_list(request):
    """Список статей с поиском и пагинацией"""
    # Получаем поисковый запрос
    query = request.GET.get('q', '').strip()

    # Фильтруем статьи
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts_list = Post.objects.all().order_by('-created_at')

    # Пагинация
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Контекст для шаблона
    context = {
        'posts': posts,
        'query': query,
    }

    # ВАЖНО: путь posts/post_list.html, а не blog/post_list.html
    return render(request, 'posts/post_list.html', context)

def post_detail(request, post_id):
    # Получаем статью или 404
    post = get_object_or_404(Post, id=post_id)
    
    # Получаем ВСЕ комментарии этой статьи
    comments = post.comments.all().order_by('-created_at')
    
    # Обработка формы
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Сохраняем, но НЕ в базу пока
            comment = form.save(commit=False)
            # Устанавливаем статью для комментария
            comment.post = post
            # Сохраняем в базу
            comment.save()
            # Перенаправляем на ту же страницу (чтобы очистить форму)
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    # Увеличиваем счётчик просмотров (добавим позже)
    # post.views += 1
    # post.save()
    
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


class PostViewSet(viewsets.ModelViewSet):
    """API для статей"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
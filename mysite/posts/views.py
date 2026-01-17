# posts/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post
from rest_framework import viewsets
from .serializers import PostSerializer

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
    """Одна статья"""
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})

class PostViewSet(viewsets.ModelViewSet):
    """API для статей"""
    queryset = Post.objects.all()
    serializer_class = PostSerializergit add .
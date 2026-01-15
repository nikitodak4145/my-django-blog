# posts/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q
from .models import Post

def post_list(request):
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
    
    return render(request, 'posts/post_list.html', context)
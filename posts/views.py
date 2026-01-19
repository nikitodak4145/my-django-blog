# posts/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Post, Comment
from django.db.models import Avg
from rest_framework import viewsets
from .serializers import PostSerializer
from .forms import CommentForm  
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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

    # СТАТИСТИКА для панели ← ДОБАВЬ ЭТОТ КОД
    all_posts = Post.objects.all()
    total_views = sum(p.views for p in all_posts)
    total_posts = all_posts.count()
    total_comments = Comment.objects.count()

    # Контекст для шаблона
    context = {
        'posts': posts,
        'query': query,
        'total_views': total_views,      # ← ДОБАВЬ
        'total_posts': total_posts,      # ← ДОБАВЬ
        'total_comments': total_comments, # ← ДОБАВЬ
    }

    return render(request, 'posts/post_list.html', context)

def post_detail(request, post_id):
    """Страница статьи с гибридным подсчётом просмотров"""
    post = get_object_or_404(Post, id=post_id)
    
    # ГИБРИД: увеличиваем просмотры только если НЕ AJAX
    # (AJAX запрос придёт отдельно из JS)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    
    if not is_ajax:
        # Обычный запрос (пользователь открыл страницу)
        post.increment_views()
    
    # Остальной код (комментарии, форма)...
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'post_id': post.id,  # Для JS
    })

class PostViewSet(viewsets.ModelViewSet):
    """API для статей"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def analytics(request):
    """Страница расширенной аналитики"""
    if not request.user.is_staff:  # Только для админов
        return redirect('post_list')
    
    posts = Post.objects.all().order_by('-views')[:10]
    total_stats = {
        'total_views': sum(p.views for p in Post.objects.all()),
        'total_posts': Post.objects.count(),
        'total_comments': Comment.objects.count(),
        'avg_views': Post.objects.aggregate(Avg('views'))['views__avg'] or 0,
        'most_popular': Post.objects.order_by('-views').first(),
    }
    
    return render(request, 'posts/analytics.html', {
        'posts': posts,
        'stats': total_stats,
        'today': timezone.now().date(),
    })


@csrf_exempt  # Временно отключаем CSRF для простоты
def api_increment_views(request, post_id):
    """API для увеличения просмотров (для JS)"""
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            new_views = post.increment_views()
            return JsonResponse({
                'success': True,
                'post_id': post_id,
                'new_views': new_views,
                'message': f'Просмотры увеличены до {new_views}'
            })
        except Post.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Статья не найдена'
            }, status=404)
    
    return JsonResponse({
        'success': False,
        'error': 'Только POST запросы'
    }, status=400)



from django.shortcuts import render
from .models import Article, Category, Tag, Comment
from django.core.paginator import Paginator


def index_handler(request):
    last_articles = Article.objects.all().order_by('-pub_date')[:6].prefetch_related('categories')
    current_page = int(request.GET.get('page', 1))
    articles_on_page = 1
    paginator = Paginator(last_articles,articles_on_page)
    page_obj =paginator.get_page(current_page)

    context = {
        'page_obj': page_obj,
        'paginator': paginator
    }
    return render(request, 'news/index.html', context)


def photo_gallery_handler(request):
    context = {}
    return render(request, 'photo-gallery.html', context)


def contact_us_handler(request):
    context = {'h1': 'Articles Database'}
    return render(request, 'news/contact-us.html', context)


def post_handler(request, slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        data = {x[0]: x[1] for x in request.POST.items()}
        data.pop('csrfmiddlewaretoken')
        data.pop('submit')
        data['article'] = article
        Comment.objects.create(**data)
    context = {'article' : article}
    return render(request, 'news/post.html', context)




def error_404_handler(request):
    context = {}
    return render(request, 'news/error-404.html', status=404)


def robots_handler(request):
    context = {}
    return render(request, 'news/robots.txt', context, content_type='text/plain')


def category_handler(request, slug):
    last_articles = Article.objects.filter(categories__slug=slug). \
                        order_by('-pub_date')[:6].prefetch_related('categories')|\
                    Article.objects.filter(author__name=slug). \
                        order_by('-pub_date')[:6].prefetch_related('authors')

    context = {'last_articles': last_articles,
               'slug':slug}
    return render(request, 'news/category.html', context)

# def header_handler(request,slug):
#     cat_list = Category.objects.annotate\
#         (count=Count('article')).order_by('count')[:5]
#     context = {'categories': cat_list}
#     return render(request, 'chunks/header.html',context)

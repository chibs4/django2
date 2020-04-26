from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.shortcuts import render
from .models import Article, Category, Tag, Comment
from django.core.paginator import Paginator
from .forms import CommentForm


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


class IndexView(TemplateView):
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_articles'] = Article.objects.all().order_by('-pub_date')[:6].prefetch_related('categories')
        return context


class PhotoGalleryView(TemplateView):

    tamplate_name =  'photo-gallery.html'

class ContactView(TemplateView):

    tamplate_name = 'news/contact-us.html'


def post_handler(request, slug):
    article = Article.objects.get(slug=slug)
    context = {'article': article}
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['article'] = article
            Comment.objects.create(**data)
        else:
            messages.add_message(request, messages.INFO, 'Error in FORM fields')
    else:
        form =CommentForm()
    context['form'] = form
    return render(request, 'news/post.html', context)

class CategoryListView(ListView):
    template_name = 'news/category.html'
    model = Article
    ordering = '-pub_date'
    paginate_by = 5



class Error404View(TemplateView):

    tamplate_name = 'news/error-404.html'

class RobotsView(TemplateView):

    tamplate_name = 'news/robots.html'
    content_type = 'text/plain'


def category_handler(request, slug):
    last_articles = Article.objects.filter(categories__slug=slug). \
                        order_by('-pub_date')[:6].prefetch_related('categories')|\
                    Article.objects.filter(author__name=slug). \
                        order_by('-pub_date')[:6].prefetch_related('authors')

    context = {'last_articles': last_articles,
               'slug':slug}
    return render(request, 'news/category.html', context)



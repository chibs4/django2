from threading import Thread

from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin
from .models import Author, Article, Comment, Category, Tag


# def get_fresh_news(modeladmin,request,queryset):
#     for object in queryset:
#         if object.name == 'Skysports':
#             Thread(target=skysports_crawler, args=()).start()
# get_fresh_news.short_description = 'Get fresh articles'


class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content,short_description')
    list_display = ('name', 'pub_date', 'author', 'image_code')
    search_fields = ('name',)
    list_filter = ('author', 'pub_date', 'categories')

    def image_code(self, object):
        return format_html('<img src="{}" style="max-width: 100px" />',
                           object.main_image.url)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'in_menu', 'articles_count')
    list_editable = ('in_menu',)
    search_fields = ('name',)

    # list_filter = ('articles_count',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('article_set')

    def articles_count(self, object):
        return object.article_set.all().count()

class AutorArticleInLine(admin.TabularInline):
    model = Article
    exclude = ('content','short_description')



class AuthorAdmin(SummernoteModelAdmin):
    list_display = ('name', 'ava')
    search_fields = ('name',)
    inlines = (AutorArticleInLine,)
    # actions = (get_fresh_news,)

    def ava(self, object):
        return format_html('<img src="{}" style="max-width: 70px" />',
                           object.avatar.url)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Tag)

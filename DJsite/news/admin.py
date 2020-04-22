from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content,short_description')

from .models import *

admin.site.register(Article,ArticleAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Tag)


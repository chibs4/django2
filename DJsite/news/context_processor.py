from django.db.models import Count
from .models import Category

def menu_categories(request):
    cat_list = Category.objects.annotate \
                   (count=Count('article')).exclude(in_menu=True).order_by('-count')[:5]

    return {'cats_list': cat_list}
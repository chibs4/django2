"""DJsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from news.views import index_handler, blog_handler, photo_gallery_handler, post_handler, contact_us_handler, \
    error_404_handler,robots_handler,header_handler

urlpatterns = [
                  path('', index_handler),
                  path('blog/', blog_handler),
                  path('photo-gallery/', photo_gallery_handler),
                  path('post/', post_handler),
                  path('contact-us/', contact_us_handler),
                  path('error-404/', error_404_handler),
path('summernote/', include('django_summernote.urls')),
                  path('admin/', admin.site.urls),
                  path('robots.txt/',robots_handler),
                  path('header/',header_handler)
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




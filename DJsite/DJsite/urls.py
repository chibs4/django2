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
from news.views import index_handler, PhotoGalleryView, post_handler, ContactView, \
    Error404View,RobotsView,CategoryListView

urlpatterns = [
                  path('', index_handler,name = 'homepage'),
                  path('category/<slug>',CategoryListView.as_view(),name = 'category'),
                  path('photo-gallery/', PhotoGalleryView.as_view() ),
                  path('post/<slug>', post_handler, name = 'post'),
                  path('contact-us/', ContactView.as_view(), name = 'contact-us'),
                  path('error-404/', Error404View.as_view()),


                  path('summernote/', include('django_summernote.urls')),
                  path('admin/', admin.site.urls),
                  path('robots.txt/',RobotsView.as_view()),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




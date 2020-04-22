from django.shortcuts import render

def blog_handler(request):
    context = {}
    return render(request, 'news/blog.html', context)

def photo_gallery_handler(request):
    context = {}
    return render(request, 'photo-gallery.html', context)

def contact_us_handler(request):
    context = {}
    return render(request, 'news/contact-us.html', context)

def post_handler(request):
    context = {}
    return render(request, 'news/post.html', context)

def index_handler(request):
    context = {}
    return render(request, 'news/index.html', context)

def error_404_handler(request):
    context = {}
    return render(request, 'news/error-404.html', status=404)

def robots_handler(request):
    context = {}
    return render(request, 'news/robots.txt', context, content_type='text/plain')

def header_handler(request):
    context = {}
    return render(request, 'chunks/header.html', context)
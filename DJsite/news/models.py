from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True,default=1)
    in_menu = models.BooleanField(default=False)
    order = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Author(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='images/avatars')
    bio = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    content = models.TextField()
    short_description = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='images')
    pub_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(to=Category)
    author = models.ForeignKey(to=Author,on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()
    article = models.ForeignKey(to=Article,on_delete=models.CASCADE, related_name='comments')

    objects = models.Manager()

    def __str__(self):
        return self.comment[:21]


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    articles = models.ManyToManyField(to=Article)

    objects = models.Manager()

    def __str__(self):
        return self.name

class Mag(models.Model):
    name = models.CharField(max_length=255)



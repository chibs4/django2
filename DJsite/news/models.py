from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    shug = models.SlugField()
    in_menu = models.BooleanField(default=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Author(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='images/avatars')
    bio = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField()
    short_description = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='images')
    pub_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(to=Category)
    author = models.ForeignKey(to=Author,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.CharField(max_length=255)
    comment = models.TextField()
    article = models.ForeignKey(to=Article,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment[:20]


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    articles = models.ManyToManyField(to=Article)

    def __str__(self):
        return self.name



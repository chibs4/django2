# Generated by Django 3.0.5 on 2020-04-22 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='article',
            name='main_image',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(upload_to='images/avatars'),
        ),
    ]

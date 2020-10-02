from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    title = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.title


class Book(models.Model):
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


    title = models.CharField(max_length=50,
                             verbose_name='Название',
                             help_text='help text',
                             db_index=True
                             )
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    text = models.TextField(verbose_name='Текст')
    author = models.ManyToManyField(User, verbose_name='Автор', db_index=True)
    published_date = models.DateField(auto_now_add=True)
    genre = models.ManyToManyField('managebook.Genre', verbose_name='Жанр')
    rate = models.ManyToManyField(User, through='managebook.BookLike', related_name='rate')

    def __str__(self):
        if self.title is not None:
            return self.title
        else:
            return "Name is not defined"


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    like = models.ManyToManyField(User, related_name='Like')


class BookLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=0)

from sqlite3.dbapi2 import IntegrityError
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Avg


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
    author = models.ManyToManyField(User, verbose_name='Автор', db_index=True, related_name="book")
    published_date = models.DateField(auto_now_add=True)
    genre = models.ManyToManyField('managebook.Genre', verbose_name='Жанр')
    rate = models.ManyToManyField(User, through='managebook.BookLike', related_name='rate')
    cached_rate = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    def __str__(self):
        if self.title is not None:
            return self.title
        else:
            return "Name is not defined"


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name="comment")
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name='Книга', related_name="comment")
    like = models.ManyToManyField(
        User, through='CommentLike',  related_name='like', blank=True, null=True)


class BookLike(models.Model):
    class Meta:
        unique_together = ["user", "book"]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_like")
    rate = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            br = BookLike.objects.get(user=self.user, book=self.book)
            br.rate = self.rate
            br.save()
        else:
            self.book.cached_rate = self.book.book_like.aggregate(Avg('rate'))['rate__avg']
            self.book.save()

class CommentLike(models.Model):
    class Meta:
        unique_together = ["comment", "user"]

    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_like")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_like")

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            CommentLike.objects.get(
                comment_id=self.comment.id, user_id=self.user.id).delete()
            self.comment.cached_like -= 1
            flag = False
        else:
            self.comment.cached_like += 1
            flag = True
        self.comment.save()
        return flag

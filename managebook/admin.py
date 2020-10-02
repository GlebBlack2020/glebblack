from django.contrib import admin
from managebook.models import Genre, Book

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'published_date']
    search_fields = ['title']
    list_filter = ['published_date', 'author', 'genre']


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)


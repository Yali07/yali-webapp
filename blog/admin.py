from django.contrib import admin
from .models import BlogPost, Comment, Category, Subscribe, NewsLetter
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Category)

admin.site.register(Subscribe)
admin.site.register(NewsLetter)


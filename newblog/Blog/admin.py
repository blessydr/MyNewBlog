from django.contrib import admin

from .models import Blog_Post, Tag,Comments
admin.site.register(Tag)
admin.site.register(Blog_Post)
admin.site.register(Comments)
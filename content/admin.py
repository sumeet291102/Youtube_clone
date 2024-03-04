from django.contrib import admin

# Register your models here.
from .models import Video, Like, Comment, Subscribe
admin.site.register(Video)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Subscribe)

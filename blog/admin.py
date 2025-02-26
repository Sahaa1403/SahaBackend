from django.contrib import admin
from blog.models import PostComment,Post


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('sender', 'create_at')
admin.site.register(PostComment, PostCommentAdmin)



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'slug', 'author', 'post_date')
admin.site.register(Post, PostAdmin)
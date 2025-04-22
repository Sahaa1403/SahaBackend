from django.contrib import admin
from search.models import SearchData,Label,KnowledgeBase,Source,SocialMedia,KnowledgeBaseLabelUser

class SourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'created_at')
    list_filter = ("created_at",)
    search_fields = ['title', 'description']
admin.site.register(Source, SourceAdmin)

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'created_at')
    list_filter = ("created_at",)
    search_fields = ['title', 'description']
admin.site.register(SocialMedia, SocialMediaAdmin)


class SearchDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'created_at')
    list_filter = ("created_at",)
    search_fields = ['text', 'ai_answer']
admin.site.register(SearchData, SearchDataAdmin)

class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Label, LabelAdmin)

class KnowledgeBaseLabelUserAdmin(admin.ModelAdmin):
    list_display = ('knowledge_base','label','user','id')
admin.site.register(KnowledgeBaseLabelUser, KnowledgeBaseLabelUserAdmin)


class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at')
    list_filter = ("category", "created_at")
    search_fields = ['title', 'id', 'body']
admin.site.register(KnowledgeBase, KnowledgeBaseAdmin)
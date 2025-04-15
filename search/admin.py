from django.contrib import admin
from search.models import SearchData,Label,KnowledgeBase

class SearchDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'created_at')
    list_filter = ("created_at",)
    search_fields = ['text', 'ai_answer']
admin.site.register(SearchData, SearchDataAdmin)

class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Label, LabelAdmin)

class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at')
    list_filter = ("category", "created_at")
    search_fields = ['title', 'id', 'body']
admin.site.register(KnowledgeBase, KnowledgeBaseAdmin)
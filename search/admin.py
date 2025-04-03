from django.contrib import admin
from search.models import KnowledgeBase
from import_export.admin import ImportExportModelAdmin

class KnowledgeBaseAdmin(ImportExportModelAdmin):
    list_display = ('id', 'category', 'body', 'created_at')
    list_filter = ("category","created_at")
    search_fields = ['body', 'id']
admin.site.register(KnowledgeBase, KnowledgeBaseAdmin)
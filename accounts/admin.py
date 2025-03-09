from django.contrib import admin
from accounts.models import User,UserType
from import_export.admin import ImportExportModelAdmin

class UserAdmin(ImportExportModelAdmin):
    list_display = ('email', 'username', 'name', 'created_at')
    list_filter = ("created_at","user_type")
    search_fields = ['username', 'email', 'name']
    readonly_fields = ('id','updated_at', 'created_at', 'last_login', 'password')
    fields = ('id','user_type','username', 'email', 'name', 'image', 'password', 'updated_at', 'created_at','last_login')
admin.site.register(User, UserAdmin)


class UserTypeAdmin(ImportExportModelAdmin):
    list_display = ('name', 'id')
admin.site.register(UserType, UserTypeAdmin)

from django.contrib import admin

from .models import *


# Register your models here.


class ApplicationsUserAdmin(admin.ModelAdmin):
    list_display = ['id_user', 'name', 'link_user', 'data_start', 'data_end']
    list_filter = ['data_start', 'data_end']
    search_fields = ['id_user', 'name']


class AppResultAdmin(admin.ModelAdmin):
    list_display = ['number_app', 'lover', 'friend_best']


admin.site.register(ApplicationUser, ApplicationsUserAdmin)
admin.site.register(AppResult, AppResultAdmin)

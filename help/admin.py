from django.contrib import admin
from .models import Help


# Register your models here.

class HelpAdmin(admin.ModelAdmin):
    list_display = ['title', 'order_by', 'contents']


admin.site.register(Help, HelpAdmin)

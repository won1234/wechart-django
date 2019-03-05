from django.contrib import admin
from .models import Cs
# Register your models here.


class CsAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'name', 'c_or_s', 'short_content', 'sub_date', 'is_process', 'short_process_result']
    list_filter = ['c_or_s', 'is_process', 'phone']
    date_hierarchy = "sub_date"


admin.site.register(Cs, CsAdmin)

from django.contrib import admin
from .models import Profile, WechatTag, Group2, NoPayDate


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'price_group', 'mobile', 'wechat_name']


admin.site.register(Profile, ProfileAdmin)


class WechatTagAdmin(admin.ModelAdmin):
    list_display = ['wechat_tag_name', 'wechat_tag_id']


admin.site.register(WechatTag, WechatTagAdmin)


class Group2Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']


admin.site.register(Group2, Group2Admin)


class NoPayDateAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'days']


admin.site.register(NoPayDate, NoPayDateAdmin)

from django.contrib import admin
from .models import Profile, WechatTag


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'price_group', 'mobile', 'wechat_name']


admin.site.register(Profile, ProfileAdmin)


class WechatTagAdmin(admin.ModelAdmin):
    list_display = ['wechat_tag_name', 'wechat_tag_id']


admin.site.register(WechatTag, WechatTagAdmin)

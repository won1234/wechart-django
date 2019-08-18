from django.contrib import admin
from .models import Profile, WechatTag, Group2, NoPayDate, Department, Freight


# from django.contrib.auth.models import User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_name_p', 'address', 'department', 'freight', 'price_group', 'mobile', 'wechat_name']
    search_fields = ('user__username', 'user__first_name')
    list_filter = ['department']


admin.site.register(Profile, ProfileAdmin)


# class ProfileInline(admin.StackedInline):  # 将Profile加入到Admin的user表中,内联
#     model = Profile
#     can_delete = False
#
#
# class UserAdmin(admin.ModelAdmin):
#     inlines = [ProfileInline]
#     list_display = ('username', 'first_name', 'email', 'is_staff', 'is_active', 'is_superuser')
#
#
# admin.site.unregister(User)  # 去掉在admin中的注册
# admin.site.register(User, UserAdmin)  # 用UserAdmin注册user

class WechatTagAdmin(admin.ModelAdmin):
    list_display = ['wechat_tag_name', 'wechat_tag_id']


admin.site.register(WechatTag, WechatTagAdmin)


class Group2Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']


admin.site.register(Group2, Group2Admin)


class NoPayDateAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'days']


admin.site.register(NoPayDate, NoPayDateAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'number']
    ordering = ('number',)


admin.site.register(Department, DepartmentAdmin)


class FreightAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']


admin.site.register(Freight, FreightAdmin)

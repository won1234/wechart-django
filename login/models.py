from django.db import models
from django.conf import settings
from mall.models import ProductPriceGroup


class WechatTag(models.Model):
    wechat_tag_name = models.CharField(max_length=25, verbose_name="企业号标签名称")
    wechat_tag_id = models.IntegerField(null=True, blank=True, verbose_name="企业号标签ID")

    class Meta:
        ordering = ('wechat_tag_id',)
        verbose_name = 'wechatTag'
        verbose_name_plural = '企业号标签'

    def __str__(self):
        return str(self.wechat_tag_name)


# 用于管理用户的权限
class Group2(models.Model):
    name = models.CharField(max_length=25, verbose_name="权限")
    slug = models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        verbose_name_plural = '权限'

    def __str__(self):
        return str(self.name)


#  未支付时间设置
class NoPayDate(models.Model):
    name = models.CharField(max_length=25, verbose_name="名称")
    slug = models.CharField(max_length=25, null=True, blank=True)
    days = models.PositiveIntegerField(null=True, blank=True, verbose_name="天数")

    class Meta:
        verbose_name_plural = '未支付时间设置'

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)  # 和系统的user model一对一
    address = models.CharField(max_length=250, verbose_name="地址")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    wechat_name = models.CharField(max_length=25, null=True, blank=True, verbose_name="企业号个人账号")
    wechat_tag = models.ManyToManyField(WechatTag)
    price_group = models.ForeignKey(ProductPriceGroup, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='price_group',
                                    verbose_name='价格组')
    group2 = models.ManyToManyField(Group2,
                                    related_name='group2',
                                    verbose_name='权限')

    class Meta:
        ordering = ('user',)
        verbose_name = 'profile'
        verbose_name_plural = '用户2'

    def __str__(self):
        return '{}(profile)'.format(self.user.first_name)

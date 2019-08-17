#!/usr/bin/env python
# coding:utf-8

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''

import django

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()


# 导入用户profile表
def main():
    from login.models import Profile
    from django.contrib.auth.models import User  # 内置的用户model
    from mall.models import ProductPriceGroup
    f = open('login_profile.csv', mode='r', encoding='utf-8')
    for line in f:
        id, address, user_id, price_group_id, mobile, wechat_name = line.split(',')
        Profile.objects.create(id=id, address=address, user=User.objects.get(id=user_id), ProductPriceGroup=ProductPriceGroup.objects.get(id=price_group_id), mobile=mobile, wechat_name=wechat_name)
    f.close()


if __name__ == "__main__":
    main()
    print('Done!')

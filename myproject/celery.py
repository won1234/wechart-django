import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')  # 创建一个Celery事例

app.config_from_object('django.conf:settings')  # 加载项目设置中任意的定制化配置。
# 告诉 Celery 自动查找我们列举在 INSTALLED_APPS 设置中的异步应用任务。
# Celery 将在每个应用路径下查找 tasks.py 来加载定义在其中的异步任务。
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# # 允许root 用户运行celery
# platforms.C_FORCE_ROOT = True
# app.conf.beat_schedule = {
#     # 'add-every-10-seconds': {
#     #     'task': 'orders.tasks.add',
#     #     'schedule': 10.0,
#     #     'args': (16, 16)
#     # },
#     'statistics-today-orders': {
#             'task': 'orders.tasks.stat_orders_today',
#             'schedule': crontab(hour=23, minute=59),
#             # 'schedule': crontab(hour=15, minute=56),
#             # 'args': (16, 16)
#         },
# }
app.conf.timezone = "Asia/Shanghai"
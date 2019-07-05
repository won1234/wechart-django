from django.contrib import admin
from .models import Order, OrderItem

import csv
import datetime
from django.http import HttpResponse

# 订单导出CSV
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta  # 用于获取model字段
    response = HttpResponse(content_type='text/csv')  # 创建一个HttpResponse实例包含一个定制text/csv内容类型来告诉浏览器这个响应需要处理为一个CSV文件。
    # 添加一个Content-Disposition头来指示这个HTTP响应包含一个附件。
    response['Content-Disposition'] = 'attachment; \
           filename={}.csv'.format(opts.verbose_name)   # 导出的文件名
    writer = csv.writer(response)  # 创建一个CSV writer对象，该对象将会被写入response对象。
    # 动态的获取model字段通过使用模型（moedl）_meta选项的get_fields()方法。我们排除多对多以及一对多的关系。
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information  添加一个头行包含models的字段名。
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows  写入数据
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)  # 反射，取得字段的值
            if isinstance(value, datetime.datetime):   # 是否是时间对象
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = '导出CSV'  # 在模版中显示的名称


# 使用 ModelInline 来把它引用为  OrderAdmin 类的内联元素。一个内联元素允许你在同一编辑页引用模型
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'paid', 'send', 'created', 'updated', 'total_cost']
    list_filter = ['paid', 'send', 'created', 'user', 'updated']
    date_hierarchy = "created"
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)

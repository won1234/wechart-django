from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # 认证（authentication）框架的login_required装饰器
from login.models import Profile
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SelectOrdersForm
from datetime import timedelta
from django.http import HttpResponse
from django.template import loader
import codecs


# 传入查询的条件，取得数据库中的订单数据
class SqlFilter(object):
    def __init__(self, user=0, paid=0, send=0, created_start=None, created_end=None):
        self.user = user
        self.paid = paid
        self.send = send
        self.start = created_start
        self.end = created_end

    # 以QuerySET形式返回订单数据
    def sql_orders(self):
        if self.start and self.end and self.start <= self.end:  # 当开始时间和结束时间都不为空，且开始时间小于等于结束时间
            # print(self.start, self.end)    # 取得的timedate.date的时间为00：00：00，所以要查今天的话，结束时间+1天
            o0 = Order.objects.filter(created__range=(self.start, self.end + timedelta(days=1)))
        elif not self.start and self.end:  # 开始时间为空,结束时间不为空
            o0 = Order.objects.filter(created__lte=(self.end + timedelta(days=1)))
        elif not self.end and self.start:  # 结束时间为空,开始时间不为空
            o0 = Order.objects.filter(created__gte=self.start)
        else:  # 开始时间和结束时间都为空
            o0 = Order.objects.all()
        if self.user:  # 当user不为0时
            self.user = Profile.objects.get(user=(User.objects.get(id=self.user)))
            o1 = o0.filter(user=self.user)
        else:
            o1 = o0
        if self.paid:  # 判断是否支付
            if self.paid == 1:
                o2 = o1.filter(paid=True)
            if self.paid == 2:
                o2 = o1.filter(paid=False)
        else:
            o2 = o1
        if self.send:  # 判断是否发货
            if self.send == 1:
                o3 = o2.filter(send=True)
            if self.send == 2:
                o3 = o2.filter(send=False)
        else:
            o3 = o2
        return o3

    # 以[（order,order_items）,...]列表+元组形式返回订单和清单数据
    def orders_items(self):
        orders_items_list = []
        orders = self.sql_orders()
        for order in orders:
            orders_items_list.append((order, OrderItem.objects.filter(order=order)))
        return orders_items_list

    # 返回查询到的的数量与总金额
    def num_cost(self):
        orders_costs = 0
        orders = self.sql_orders()
        orders_num = len(orders)
        for order in orders:
            orders_costs = orders_costs + order.total_cost
        return (orders_num, orders_costs)


# 导出CSV功能
def export_to_csv(filter_conditon, title_row, datas, template_csv):
    # filter_conditon 过滤的条件
    # title_row标题行
    # datas 数据
    # template_csv 模版文件名
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    # codecs.BMO_UTF8解决文件内容中文乱码
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    # first_row = ('订单号', '创建时间', '下单人', '是否发货', '是否支付', '产品', '数量')

    t = loader.get_template('manager/' + template_csv)
    # c = Context({
    #     'data': csv_data,
    # })
    # print({'orders': orders_fliter, 'order_items': order_items})
    # 字典格式
    c = {'filter_conditon': filter_conditon, 'title_row': title_row, 'datas': datas}
    response.write(t.render(c))
    return response


# 导出TXT功能
def export_to_txt(filter_conditon, title_row, datas, template_csv):
    # filter_conditon 过滤的条件
    # title_row标题行
    # datas 数据
    # template_csv 模版文件名
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/plain')
    # codecs.BMO_UTF8解决文件内容中文乱码
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename="orders.txt"'

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    # first_row = ('订单号', '创建时间', '下单人', '是否发货', '是否支付', '产品', '数量')

    t = loader.get_template('manager/' + template_csv)
    # 字典格式
    c = {'filter_conditon': filter_conditon, 'title_row': title_row, 'datas': datas}
    # response.write(t.render(c))
    response.write("<p>Here's the text of the Web page.</p>")
    response.write("<p>Here's another paragraph.</p>")
    return response


@login_required
def order_list(request):
    if not request.GET.get('user') and not request.GET.get('page'):  # 通过传过来的url，判断是刚打开页面还是点了确定
        form = SelectOrdersForm()
        return render(request, 'manager/order_list.html', {'form': form})
    else:
        form = SelectOrdersForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            # 根据传过来的用户id进行判断，查找什么数据
            # cd{'user': 0, 'paid': 0, 'send': 0, 'created_start': None, 'created_end': None}
            # is_paid = ((0, '全部'), (1, '已支付'), (2, '未支付'))
            # is_send = ((0, '全部'), (1, '已发货'), (2, '未发货'))
            # 传入条件，创建查询数据库的实例
            orders_sql = SqlFilter(cd['user'], cd['paid'], cd['send'], cd['created_start'], cd['created_end'])
            # 查询数据，取得的是个列表
            orders_items_list = orders_sql.orders_items()
            # print('request.scheme', request.scheme)
            # print('request.path', request.path)
            # print('request.encoding', request.encoding)
            # print('request.META', request.META)
            # 导出为cvs
            if request.GET['export_csv'] == 'on':
                title_row = ('订单号', '创建时间', '下单人', '是否发货', '是否支付', '产品', '数量')
                return export_to_csv(filter_conditon=orders_sql, title_row=title_row, datas=orders_items_list,
                                     template_csv='orders_manager.csv')

            else:
                # 使用paginator 分页，点一次分页，执行一次这个函数，只是展示的时候不进行展示
                # global paginator
                paginator = Paginator(orders_items_list, 15)  # 每页5条
                page = request.GET.get('page')  # html 传过来的页数
                # print('page', page)
                try:
                    orders_items_list = paginator.page(page)  # 返回orders为page对象
                except PageNotAnInteger:  # 当向page()提供一个不是整数的值时抛出。
                    orders_items_list = paginator.page(1)  # 如果page不是一个整数，返回第一页
                except EmptyPage:  # 当向page()提供一个有效值，但是那个页面上没有任何对象时抛出。
                    orders_items_list = paginator.page(paginator.num_pages)  # 如果page数量超过返回，发送最后一页的值
                return render(request, 'manager/order_list.html',
                              {'orders_items_list': orders_items_list, 'form': form, 'url_get': request.GET})


# 用于管理员查看,含订单金额页面，报表导出功能；
@login_required
def order_list_cost(request):
    if not request.GET.get('user') and not request.GET.get('page'):  # 通过传过来的url，判断是刚打开页面还是点了确定
        form = SelectOrdersForm()
        # print('456')
        return render(request, 'manager/order_list_cost.html', {'form': form})
    else:
        # print('678')
        # print(request.GET)
        form = SelectOrdersForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            # 根据传过来的用户id进行判断，查找什么数据
            # cd{'user': 0, 'paid': 0, 'send': 0, 'created_start': None, 'created_end': None}
            # is_paid = ((0, '全部'), (1, '已支付'), (2, '未支付'))
            # is_send = ((0, '全部'), (1, '已发货'), (2, '未发货'))
            # 传入条件，创建查询数据库的实例
            orders_sql = SqlFilter(cd['user'], cd['paid'], cd['send'], cd['created_start'], cd['created_end'])
            # 查询数据，取得的是个列表
            orders_items_list = orders_sql.orders_items()
            if request.GET['export_csv'] == 'on':  # 导出cvs
                # print('export csv')
                # filter_conditon = orders_sql
                title_row = ('订单号', '创建时间', '下单人', '订单金额', '是否发货', '是否支付', '产品', '数量', '单价', '总价')
                # datas = orders_items_list
                # template_csv = 'orders_manager.csv'
                return export_to_csv(filter_conditon=orders_sql, title_row=title_row, datas=orders_items_list,
                                     template_csv='order_list_cost.csv')
            else:
                # 使用paginator 分页，点一次分页，执行一次这个函数，只是展示的时候不进行展示
                # global paginator
                paginator = Paginator(orders_items_list, 15)  # 每页5条
                page = request.GET.get('page')  # html 传过来的页数
                # print('page', page)
                try:
                    orders_items_list = paginator.page(page)  # 返回orders为page对象
                except PageNotAnInteger:  # 当向page()提供一个不是整数的值时抛出。
                    orders_items_list = paginator.page(1)  # 如果page不是一个整数，返回第一页
                except EmptyPage:  # 当向page()提供一个有效值，但是那个页面上没有任何对象时抛出。
                    orders_items_list = paginator.page(paginator.num_pages)  # 如果page数量超过返回，发送最后一页的值
                return render(request, 'manager/order_list_cost.html',
                              {'orders_items_list': orders_items_list, 'form': form, 'url_get': request.GET})

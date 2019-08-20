from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # 认证（authentication）框架的login_required装饰器
from login.models import Profile
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SelectOrdersForm
from datetime import timedelta, datetime
from django.http import HttpResponse, FileResponse
from django.template import loader
import codecs
from reportlab.pdfgen import canvas
import io


# 传入查询的条件，取得数据库中的订单数据
class SqlFilter(object):
    '''
        传入参数 ：user用户id（int），
                    paid（0，1，2）(0, '全部'), (1, '已支付'), (2, '未支付')， int
                    send（0，1，2）(0, '全部'), (1, '已发货'), (2, '未发货')   int
                    created_start订单的开始时间，    可以是如‘2018-08-01’字符串, 也可以是datetime对象
                    created_end订单的结束时间 ，
        获得的数据： self.user Profile用户实例，
                    SqlFilter.sql_orders()   订单的queryset
                    SqlFilter.orders_items()   以[（order,order_items）,...]列表+元组形式返回订单和清单数据
                    SqlFilter.num_cost()    查询到的的数量与总金额return (orders_num, orders_costs)
    '''

    def __init__(self, user=0, paid=0, send=0, created_start=None, created_end=None):
        self.user = user
        self.paid = paid
        self.send = send
        self.start = created_start  # html 传过来的数据类型 None <class 'NoneType'> / 2019-07-01 <class 'datetime.date'>
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

    # 以[（order,order_items）,...]列表+元组形式返回订单和清单数据 order_items为queryset
    def orders_items(self):
        orders_items_list = []
        orders = self.sql_orders()
        for order in orders:
            orders_items_list.append((order, OrderItem.objects.filter(order=order)))
        return orders_items_list

    # 返回查询到的订单数量与总金额
    def num_cost(self):
        orders_costs = 0
        orders = self.sql_orders()
        orders_num = len(orders)
        for order in orders:
            orders_costs = orders_costs + order.get_total_cost()
        return (orders_num, orders_costs)

    # 返回查询到的订单，每样产品的｛总量，订单个数，（管理员+描述：数量），金额｝
    def products_total(self):
        products_total_dic = {}  # {product:{'total': , 'num': , 'details': ,'cost':,},....}
        for orders_items in self.orders_items():
            order = orders_items[0]
            if order.user.user.is_superuser:  # 判断是否是超级管理员，返回为true和false
                order_detail = str(order.description)
            else:
                order_detail = order.user.user.first_name
            order_items = orders_items[1]
            for order_item in order_items:  # 每条item
                product = order_item.product
                quantity = order_item.quantity
                price = order_item.price
                product_existed = products_total_dic.get(product)  # 如果已经存在返回字典中的内容，否则返回None
                if product_existed:
                    product_existed['total'] = product_existed['total'] + quantity
                    product_existed['num'] = product_existed['num'] + 1
                    product_existed['details'] = product_existed['details'] + ' ，（' + order_detail + ':' + str(
                        quantity) + ')'
                    product_existed['cost'] = product_existed['cost'] + quantity * price
                else:  # 如果字典中不存在这个product
                    detail = '（' + order_detail + ':' + str(quantity) + ')'
                    products_total_dic[product] = {'total': quantity, 'num': 1, 'details': detail,
                                                   'cost': quantity * price}
        return products_total_dic

    # 返回每个用户的统计字典{user: {'orders':[（order,order_items),...], 'products_list_sorted':[],'orders_num': , 'cost': },...}
    def user_orders_total(self):
        users_orders_total_dic = {}
        for order, order_items in self.orders_items():
            user_profile = order.user
            user_orders_total_dic = users_orders_total_dic.get(user_profile, {'orders': [], 'orders_num': 0,
                                                                              'cost': 0})  # 用户还不存在，初始化，如果存在进行赋值
            user_orders_total_dic['orders'].append((order, order_items))
            user_orders_total_dic['orders_num'] = user_orders_total_dic['orders_num'] + 1
            user_orders_total_dic['cost'] = user_orders_total_dic['cost'] + order.get_total_cost()
            users_orders_total_dic[user_profile] = user_orders_total_dic
        return users_orders_total_dic


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
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = (
        ('First row', 'Foo', 'Bar', 'Baz'),
        ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
    )

    t = loader.get_template('manager/my_template_name.txt')
    response.write(t.render({'data': csv_data}))
    return response


# 导出PDF
def export_to_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    # buffer用来代替文件来存储pdf文档, 在使用FileResponse返回之前，您需要将流位置重置为其开头：
    buffer.seek(io.SEEK_SET)
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


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
                title_row = ('订单号', '创建时间', '下单人', '是否发货', '是否支付', '产品', '数量', '订单描述')
                return export_to_csv(filter_conditon=orders_sql, title_row=title_row, datas=orders_items_list,
                                     template_csv='orders_manager.csv')
                # return export_to_pdf(request)

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
            # 查询数据，取得的是个列表 ，[（order,order_items）,...]列表+元组形式返回订单和清单数据
            orders_items_list = orders_sql.orders_items()
            if request.GET['export_csv'] == 'on1':  # 导出cvs1
                # print('export csv')
                # filter_conditon = orders_sql
                title_row = ('订单号', '创建时间', '下单人', '订单金额', '是否发货', '是否支付', '产品', '数量', '单价', '总价', '订单描述')
                # datas = orders_items_list
                # template_csv = 'orders_manager.csv'
                return export_to_csv(filter_conditon=orders_sql, title_row=title_row, datas=orders_items_list,
                                     template_csv='order_list_cost.csv')
            elif request.GET['export_csv'] == 'on2':  # 导出cvs2
                title_row = ('产品', '数量', '单价', '总价')
                # 根据用户对订单进行分组
                order_user_dic = {}
                # { user1:{
                #           'order_list':[（order,order_items）, ...,],  # 用户的订单s
                #           'total_cost':     # 该用户所有订单的总金额
                #           },
                #   ...,
                #  user: {..}
                # }
                for order_tuple in orders_items_list:
                    user = order_tuple[0].user  # 取得订单的用户
                    order_user_existed = order_user_dic.get(user)  # 用于判断订单中是否含有这个用户
                    if order_user_existed:
                        order_user_dic[user]['order_list'].append(order_tuple)  # 添加到列表中
                        order_user_dic[user]['total_cost'] = order_user_dic[user]['total_cost'] + order_tuple[
                            0].get_total_cost()
                    else:
                        order_user_dic[user] = {'order_list': [order_tuple],
                                                'total_cost': order_tuple[0].get_total_cost()}
                return export_to_csv(filter_conditon=orders_sql, title_row=title_row, datas=order_user_dic,
                                     template_csv='order_list_cost_2.csv')
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


# 今日订单 展示当天的数据，每样东西总计，有哪些订单，哪些东西；
@login_required
def orders_today(request):
    today_datetime = datetime.today()
    today_date = today_datetime.strftime("%Y-%m-%d")
    # 传入条件，创建查询数据库的实例
    orders_sql = SqlFilter(created_start=today_date)
    # 查询数据，取得的是个列表
    orders_items_list = orders_sql.orders_items()
    # 订单统计
    products_total = orders_sql.products_total()
    # 根据产品id对字典进行排序，返回一个列表
    products_total_list = sorted(products_total.items(), key=lambda x: x[0].id)
    return render(request, 'manager/orders_today.html',
                  {'orders_items_list': orders_items_list, 'today_datetime': today_datetime,
                   'products_total': products_total_list})


# 展示一段时间，表和折线图。店铺和全部的统计。不选时间，默认为最近15天。
@login_required
def shop_statistical_table(request):
    if request.method == 'POST':  # 点击提交时，取得用户profile的id和日期。
        form = SelectOrdersForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # 根据传过来的用户id进行判断，查找什么数据
            # cd{'user': 0, 'paid': 0, 'send': 0, 'created_start': None, 'created_end': None}
            # is_paid = ((0, '全部'), (1, '已支付'), (2, '未支付'))
            # is_send = ((0, '全部'), (1, '已发货'), (2, '未发货'))
            # print(cd['user'], type(cd['user']))  # 0 <class 'int'>
            if not cd['created_start']:  # 如果提交的开始时间为空时,开始时间为当前时间-15天
                cd['created_start'] = datetime.today() - timedelta(days=15)
            if not cd['created_end']:   # 如果结束时间为空，则为当前时间
                cd['created_end'] = datetime.today()
            if cd['user']:  # 用户不为全部时
                user_all = False
                # 传入条件，创建查询数据库的实例
                orders_sql = SqlFilter(cd['user'], cd['paid'], cd['send'], cd['created_start'], cd['created_end'])
                # 查询数据，取得的是个列表 ，[（order,order_items）,...]列表+元组形式返回订单和清单数据
                orders_items_list = orders_sql.orders_items()
                user_name = orders_sql.user
                # start_datetime = orders_sql.start   # 输入的开始时间与结束时间
                # end_datetime = orders_sql.end
                # [product,...] {date:{product:,...},...} products_quantity_dic ={product:quantitys,...}
                products_set = set()  # 所有产品的集合
                product_quantitys_dic = {}  # 每样产品的数量总和
                product_cost_dic = {}  # 每样产品的金额总和
                date_products_dic = {}
                for order, order_items in orders_items_list:
                    order_created = order.created
                    order_created_day = datetime(order_created.year, order_created.month, order_created.day, 0, 0)
                    products_dic = date_products_dic.get(order_created_day,
                                                         {'day_cost': 0})  # 取得这个日期的添加进去的产品 {product:quantity,...}
                    for order_item in order_items:
                        product = order_item.product
                        quantity = order_item.quantity
                        price = order_item.price
                        product_quantity = products_dic.get(product, 0)  # 取得这个产品之前的数量（今天）
                        product_quantitys = product_quantitys_dic.get(product, 0)  # 取得这个产品之前的数量（所有）
                        product_cost = product_cost_dic.get(product, 0)  # 取得这个产品之前的金额（所有）
                        products_dic[product] = quantity + product_quantity  # 重新赋值产品数量
                        products_dic['day_cost'] = products_dic['day_cost'] + quantity * price  # 计算一天的金额
                        product_quantitys_dic[product] = quantity + product_quantitys
                        product_cost_dic[product] = quantity * price + product_cost
                        products_set.add(product)  # 把产品添加到集合中
                    date_products_dic[order_created_day] = products_dic
                products_list = list(products_set)
                products_list_sorted = sorted(products_list, key=lambda x: x.id)  # 根据产品的id进行排序
                total_cost = 0
                for cost in product_cost_dic.values():
                    total_cost = total_cost + cost
                # X轴时间列表。根据订单时间进行排序，开始和结束时间差，取得列表。
                date_all_sort = []
                if date_products_dic:  # 订单存在时
                    date_list = []
                    for date in date_products_dic.keys():
                        date_list.append(date)
                    date_list.sort()  # 按日期从小到大进行排序
                    t = timedelta(days=1)
                    date_start = date_list[0]
                    date_end = date_list[-1]
                    while date_start <= date_end:
                        date_all_sort.append(date_start)
                        date_start = date_start + t
                return render(request, 'manager/shop_statistical_table.html',
                              {'date_products_dic': date_products_dic, 'product_quantitys_dic': product_quantitys_dic,
                               'product_cost_dic': product_cost_dic, 'products_list_sorted': products_list_sorted,
                               'form': form, 'user_name': user_name, 'total_cost': total_cost,
                               'date_all_sort': date_all_sort, 'user_all': user_all,
                               'is_paid': cd['paid'], 'is_send': cd['send']})

            else:  # 用户为全部时
                # print(cd['created_start'], cd['created_end'])
                if cd['created_start'] and cd['created_end']:  # 时间不为空时
                    user_all = True
                    # 传入条件，创建查询数据库的实例
                    orders_sql = SqlFilter(cd['user'], cd['paid'], cd['send'], cd['created_start'], cd['created_end'])
                    total_cost = orders_sql.num_cost()[1]  # 订单总金额
                    products_total_dic = orders_sql.products_total()  # {product:{'total': , 'num': , 'details': ,'cost':,},....}
                    users_orders_total_dic = orders_sql.user_orders_total()  # 每个用户统计{user: {'orders':[（order,order_items),...], 'orders_num': , 'cost': },...}
                    return render(request, 'manager/shop_statistical_table.html',
                                  {'products_total_dic': products_total_dic,
                                   'users_orders_total_dic': users_orders_total_dic,
                                   'form': form, 'total_cost': total_cost,
                                   'start_date': cd['created_start'], 'end_date': cd['created_end'],
                                   'user_all': user_all, 'is_paid': cd['paid'], 'is_send': cd['send']})

    form = SelectOrdersForm()
    return render(request, 'manager/shop_statistical_table.html', {'form': form})

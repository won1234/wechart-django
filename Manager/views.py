from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # 认证（authentication）框架的login_required装饰器
from login.models import Profile
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SelectOrdersForm
from datetime import timedelta


@login_required
def order_list(request):
    if request.method == 'POST':
        form = SelectOrdersForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # 根据传过来的用户id进行判断，查找什么数据
            # cd{'user': 0, 'paid': 0, 'send': 0, 'created_start': None, 'created_end': None}
            # is_paid = ((0, '全部'), (1, '已支付'), (2, '未支付'))
            # is_send = ((0, '全部'), (1, '已发货'), (2, '未发货'))
            cs = cd['created_start']
            ce = cd['created_end']
            if cs and ce and cs <= ce:   # 当开始时间和结束时间都不为空，且开始时间小于等于结束时间
                # print(cs, ce)    # 取得的timedate.date的时间为00：00：00，所以要查今天的话，结束时间+1天
                o0 = Order.objects.filter(created__range=(cs, ce+timedelta(days=1)))
            elif not cs and ce:    # 开始时间为空,结束时间不为空
                o0 = Order.objects.filter(created__lte=(ce+timedelta(days=1)))
            elif not ce and cs:    # 结束时间为空,开始时间不为空
                o0 = Order.objects.filter(created__gte=cs)
            else:                   # 开始时间和结束时间都为空
                o0 = Order.objects.all()
            if cd['user']:
                o1 = o0.filter(user=Profile.objects.get(user=(User.objects.get(id=cd['user']))))
            else:
                o1 = o0
            if cd['paid']:
                if cd['paid'] == 1:
                    o2 = o1.filter(paid=True)
                if cd['paid'] == 2:
                    o2 = o1.filter(paid=False)
            else:
                o2 = o1
            if cd['send']:
                if cd['send'] == 1:
                    orders_fliter = o2.filter(send=True)
                if cd['send'] == 2:
                    orders_fliter = o2.filter(send=False)
            else:
                orders_fliter = o2
            # 取得每个订单对应的清单数据
            order_items = {}
            for order in orders_fliter:
                order_items[order] = OrderItem.objects.filter(order=order)
                # 使用paginator 分页
                paginator = Paginator(orders_fliter, 15)  # 每页5条
                page = request.GET.get('page')  # html 传过来的页数
                try:
                    orders = paginator.page(page)  # 返回orders为page对象
                except PageNotAnInteger:  # 当向page()提供一个不是整数的值时抛出。
                    orders = paginator.page(1)  # 如果page不是一个整数，返回第一页
                except EmptyPage:  # 当向page()提供一个有效值，但是那个页面上没有任何对象时抛出。
                    orders = paginator.page(paginator.num_pages)  # 如果page数量超过返回，发送最后一页的值
            return render(request, 'manager/order_list.html',
                          {'orders': orders_fliter, 'order_items': order_items, 'form': form})
    form = SelectOrdersForm()
    return render(request, 'manager/order_list.html', {'form': form})
# todo 加入是否已经发货，是否收款功能。
# 根据权限进行判断，是否展示确认功能
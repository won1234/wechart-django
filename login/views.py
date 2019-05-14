from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse  # 渲染页面，重定向网页
from django.contrib.auth import authenticate, login, logout  # django的认证框架
from .forms import LoginForm  # 导入自建的forms.py中的LoginForm类
from orders.models import Order, OrderItem
from .models import Profile, NoPayDate
from datetime import date, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # 提交的数据实例化表单（form）
        if form.is_valid():  # 检查这个表单是否有效
            cd = form.cleaned_data  # 取得数据
            # 使用authenticate()方法通过数据库对这个用户进行认证（authentication）
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:  # 如果用户存在
                today = date.today()  # 当前日期
                user_pro = Profile.objects.get(user=user)  # 取得自定义的用户信息
                #  取得未支付时间设置/nologin（禁止登录）/forbidden(禁止购买)/remind（提醒）
                nologindate = today + timedelta(days=-NoPayDate.objects.get(
                    slug='nologin').days)  # 取得多少时间以前还有未支付的订单，禁止登录 datetime.date(2019, 5, 11)
                orders_no_pay = Order.objects.filter(user=user_pro).filter(paid=False)  # 未支付的订单
                if orders_no_pay.filter(created__lte=nologindate):  # 判断禁止登录时间之前的订单有没有
                    # 展示未支付的订单个金额
                    no_pay_order_id = ''
                    no_pay_total = 0
                    for order_no_pay in orders_no_pay:
                        order_items = OrderItem.objects.filter(order=order_no_pay)
                        for order_item in order_items:
                            no_pay_total += order_item.get_cost()
                        no_pay_order_id = str(order_no_pay.id) + '；' + no_pay_order_id
                    no_pay_dic = {'no_pay_order_id': no_pay_order_id, 'no_pay_total': no_pay_total}
                    # 使用paginator 分页
                    paginator = Paginator(orders_no_pay, 15)  # 每页5条
                    page = request.GET.get('page')  # html 传过来的页数
                    try:
                        orders = paginator.page(page)  # 返回orders为page对象
                    except PageNotAnInteger:  # 当向page()提供一个不是整数的值时抛出。
                        orders = paginator.page(1)  # 如果page不是一个整数，返回第一页
                    except EmptyPage:  # 当向page()提供一个有效值，但是那个页面上没有任何对象时抛出。
                        orders = paginator.page(paginator.num_pages)  # 如果page数量超过返回，发送最后一页的值
                    # 取得每个订单对应的清单数据
                    order_items = {}
                    for order in orders:
                        order_items[order] = OrderItem.objects.filter(order=order)
                    return render(request, 'orders/order/order_list.html',
                                  {'orders': orders, 'order_items': order_items, 'no_pay_dic': no_pay_dic,
                                   'nologindate': nologindate.strftime('%Y-%m-%d')})
                # 用户登录
                if user.is_active:  # 如果用户的状态是active
                    login(request, user)  # 调用login()方法集合用户到会话（session）
                    return redirect(reverse('mall:product_list'))  # 重定向网页，到mall
                else:
                    return render(request, 'registrtion/login.html', {'form': form})
            else:
                return render(request, 'registrtion/login.html', {'form': form})
    else:
        form = LoginForm()  # 为GET时，传入LoginForm为空
    return render(request, 'registrtion/login.html', {'form': form})  # 无论如何最终都要返回


def user_logout(request):
    logout(request)
    return HttpResponse('登出成功！')



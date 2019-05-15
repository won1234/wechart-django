from django.shortcuts import render
from .models import OrderItem
# from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.auth.decorators import login_required  # 认证（authentication）框架的login_required装饰器
from login.models import Profile
from django.contrib.auth.models import User
from .models import Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# # 创建订单
# @login_required
# def order_create(request):
#     cart = Cart(request)   # 获取到当前会话中的购物车。
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()  # 创建一个新的 Order 实例
#             # 保存进数据库中
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                                          product=item['product'],
#                                          price=item['price'],
#                                          quantity=item['quantity'])
#             # clear the cart
#             cart.clear()  # 清空购物车
#             order_created.delay(order.id)  # 启动发送订单信息的异步任务,调用任务的 delay() 方法并异步地执行它。
#             return render(request,
#                           'orders/order/created.html',
#                           {'order': order})
#     else:
#         form = OrderCreateForm()   # GET 请求：实例化 OrderCreateForm 表单然后渲染模板 orders/order/create.html
#     return render(request,
#                   'orders/order/create.html',
#                   {'cart': cart, 'form': form})


# 创建订单
@login_required
def order_create(request):
    cart = Cart(request)  # 获取到当前会话中的购物车。
    # 获取当前用户
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        # form = OrderCreateForm({'user': user})
        # if form.is_valid():
        #     order = form.save()  # 创建一个新的 Order 实例
        #     # 保存进数据库中
        #     for item in cart:
        #         OrderItem.objects.create(order=order,
        #                                  product=item['product'],
        #                                  price=item['price'],
        #                                  quantity=item['quantity'])
        #     # clear the cart
        #     cart.clear()  # 清空购物车
        #     order_created.delay(order.id)  # 启动发送订单信息的异步任务,调用任务的 delay() 方法并异步地执行它。
        #     return render(request,
        #                   'orders/order/created.html',
        #                   {'order': order})
        # 创建订单
        order = Order.objects.create(user=user, total_cost=cart.get_total_price())  # 返回的是对象
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        # 清空购物车
        cart.clear()
        order_created.delay(order.id)  # 启动发送订单信息的异步任务,调用任务的 delay() 方法并异步地执行它。
        return render(request,
                      'orders/order/created.html',
                      {'order': order})

    #
    # else:
    #     form = OrderCreateForm({
    #
    #     }
    #
    #     )   # GET 请求：实例化 OrderCreateForm 表单然后渲染模板 orders/order/create.html
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'user_profile': user_profile})


# todo 展示已经购买我的订单
@login_required
def order_list(request):
    # 获取当前用户
    user = User.objects.get(username=request.user.username)
    orders_list = Order.objects.filter(user=user)  # 取得用户的所有订单
    # 使用paginator 分页
    paginator = Paginator(orders_list, 2)  # 每页5条
    page = request.GET.get('page')   # html 传过来的页数
    try:
        orders = paginator.page(page)   # 返回orders为page对象
    except PageNotAnInteger:             # 当向page()提供一个不是整数的值时抛出。
        orders = paginator.page(1)    # 如果page不是一个整数，返回第一页
    except EmptyPage:                   # 当向page()提供一个有效值，但是那个页面上没有任何对象时抛出。
        orders = paginator.page(paginator.num_pages)        # 如果page数量超过返回，发送最后一页的值
    # 取得每个订单对应的清单数据
    order_items = {}
    for order in orders:
        order_items[order] = OrderItem.objects.filter(order=order)
    return render(request, 'orders/order/order_list.html', {'orders': orders, 'order_items': order_items})

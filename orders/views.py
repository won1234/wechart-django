from django.shortcuts import render
from .models import OrderItem
from .forms import AdminCreateOrder
from cart.cart import Cart
from .tasks import order_created
from django.contrib.auth.decorators import login_required  # 认证（authentication）框架的login_required装饰器
from login.models import Profile
from django.contrib.auth.models import User
from .models import Order
from mall.models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 创建订单
@login_required
def order_create(request):
    cart = Cart(request)  # 获取到当前会话中的购物车。
    # 获取当前用户
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)  # 当前用户的扩展信息
    user_permissions = user_profile.group2.all()  # 用户的权限
    if request.method == 'POST':
        # 创建订单, 返回的order是对象
        description = request.POST.get('description', None)
        if description:  # total_cost已经没用了
            order = Order.objects.create(user=user_profile, total_cost=cart.get_total_price(), description=description)
        else:
            order = Order.objects.create(user=user_profile, total_cost=cart.get_total_price())
        for item in cart:  # 取得购物车中的物品清单，写入数据库
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        # 清空购物车
        cart.clear()
        order_created.delay(user_profile.id, order.id)  # 启动微信发送订单信息的异步任务,调用任务的 delay() 方法并异步地执行它。
        return render(request,
                      'orders/order/created.html',
                      {'order': order})

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'user_profile': user_profile, 'user_permissions': user_permissions})


@login_required
def order_list(request):
    # 获取当前用户
    user_pro = Profile.objects.get(user=User.objects.get(username=request.user.username))  # 当前用户的扩展信息
    orders_list = Order.objects.filter(user=user_pro)  # 取得用户的所有订单
    orders_no_pay = Order.objects.filter(user=user_pro).filter(paid=False)  # 未支付的订单
    no_pay_order_id = ''
    no_pay_total = 0
    for order_no_pay in orders_no_pay:
        no_pay_total += order_no_pay.get_total_cost()
        no_pay_order_id = str(order_no_pay.id) + '；' + no_pay_order_id
    no_pay_dic = {'no_pay_order_id': no_pay_order_id, 'no_pay_total': no_pay_total}

    # 使用paginator 分页
    paginator = Paginator(orders_list, 15)  # 每页5条
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
                  {'orders': orders, 'order_items': order_items, 'no_pay_dic': no_pay_dic})


# 管理员创建订单，选择用户，分析字符串，根据前两个字匹配产品名称。
@login_required
def admin_create_order(request):
    if request.user.username == 'won':  # 判断是否是管理员
        if request.method == 'POST':  # 点击确定时
            form = AdminCreateOrder(request.POST)
            if form.is_valid():
                user_profile_id = form.cleaned_data['user']
                order_message = form.cleaned_data['order']
                # print('user_name', user_profile_id, type(user_profile_id), 'order_message', order_message,type(order_message))
                # user_name 2 <class 'int'> order_message 肉1，笋干2 <class 'str'> 取得的值与类型
                products = Product.objects.filter(category=Category.objects.get(name='馅料'))
                name_obj_dic = {}  # key：Product name 的前两个字，value：Product对象
                name_str = ''
                for product in products:
                    name_obj_dic[product.name[:2]] = product
                    name_str = name_str + "。" + product.name[:2]
                items = []
                try:
                    for i in order_message.split('。'):  # 判断字符串的有效性
                        name_2 = i[:2]
                        num = int(i[2:])
                        items.append((name_obj_dic[name_2], num))
                except Exception as e:
                    return render(request, 'orders/order/admin_create_order.html', {'form': form, 'error': e, 'products': name_str})
                else:  # 如果字符串有效，创建订单
                    user_profile = Profile.objects.get(id=user_profile_id)  # 取得用户
                    description = '管理员代下单'
                    total_cost = 0.12
                    order = Order.objects.create(user=user_profile, total_cost=total_cost,
                                                 description=description)  # 创建订单
                    for product, quantity in items:
                        OrderItem.objects.create(order=order,
                                                 product=product,
                                                 price=product.price,
                                                 quantity=quantity)
                    form = AdminCreateOrder()  # 创建成功则清空内容
                    return render(request, 'orders/order/admin_create_order.html', {'form': form, 'error': str(order) + '下单成功'})
        else:
            form = AdminCreateOrder()  # 当为一个GET时，返回一个空Form
        return render(request, 'orders/order/admin_create_order.html', {'form': form})

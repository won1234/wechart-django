from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from mall.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartProductQuantityForm
from django.contrib.auth.decorators import login_required  # 认证（authentication）框架的login_required装饰器

# 购物车添加新的产品或者更新当前产品的数量
# require_POST 装饰器来只响应 POST 请求
@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)  # 创建一个购物车
    product = get_object_or_404(Product, id=product_id)  # 取得这个产品id的对象
    form = CartAddProductForm(request.POST)         # 把请求传给form验证数据，返回一个form对象
    if form.is_valid():
        cd = form.cleaned_data       # 取得POST上传的数据
        # 购物车中添加或者更新产品。
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

# 更新产品数量
@login_required
@require_POST
def cart_update_quantity(request, product_id):
    cart = Cart(request)  # 创建一个购物车
    product = get_object_or_404(Product, id=product_id)  # 取得这个产品id的对象
    form = CartProductQuantityForm(request.POST)         # 把请求传给form验证数据，返回一个form对象
    # print(form)
    if form.is_valid():
        cd = form.cleaned_data       # 取得POST上传的数据
        # 购物车中添加或者更新产品。
        cart.update_quantity(product=product, quantity=cd['quantity'])
    return redirect('cart:cart_detail')


# 删除购物车中的物品
@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    # 重定向到 cart_detail URL
    return redirect('cart:cart_detail')


# # 展示购物车和其中的物品。
# @login_required
# def cart_detail(request):
#     cart = Cart(request)    # 创建购物车实例
#     # CartAddProductForm 实例来允许用户改变产品的数量
#     for item in cart:
#         item['update_quantity_form'] = CartAddProductForm(
#             initial={'quantity': item['quantity'],
#                      'update': True})  # update 字段设为 True ，当提交表单到 cart_add 视图时，当前的数量就被新的数量替换了。
#     return render(request, 'cart/detail.html', {'cart': cart})

# 展示购物车和其中的物品。
@login_required
def cart_detail(request):
    cart = Cart(request)    # 创建购物车实例
    # CartProductQuantityForm 产品数量
    for item in cart:
        item['update_quantity_form'] = CartProductQuantityForm({'quantity': item['quantity']})     # 给form赋值
    return render(request, 'cart/detail.html', {'cart': cart})

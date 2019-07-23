from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required  # 认证（authentication）框架的login_required装饰器


# 检索和展示单一的品类
@login_required
def product_list(request, category_slug=None):  # 默认为none，全部展示
    # 可选参数 category_slug 通过所给产品类别来有选择性的筛选产品。
    # category_slug默认为None
    # print(
    #       # request.session['is_login'],
    #       request.user,
    #       request.user.id,
    #       '########################',
    #       dir(request.session.keys),
    #       )
    category = None
    categories = sorted(Category.objects.all(), key=lambda x: x.id)  # 取得所有品类
    # available=True 的查询集来检索可用的产品
    products = sorted(Product.objects.filter(available=True), key=lambda x: x.id)
    if category_slug:  # 如果category_slug有值传进来， 修改category
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)  # 取得对应的产品
    return render(request,
                  'mall/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


@login_required
# 检索和展示单一的产品。
def product_detail(request, id, slug):
    # product_detail 视图（view）接收 id 和 slug 参数来检索 Product 对象。
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()  # 创建form实例
    return render(request,
                  'mall/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

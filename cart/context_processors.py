from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}   # 使用 request 对象实例化了购物车

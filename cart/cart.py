from decimal import Decimal
from django.conf import settings
from mall.models import Product


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session  # 保存当前会话
        cart = self.session.get(settings.CART_SESSION_ID)  # 尝试从当前会话中获取购物车。
        if not cart:  # 当前会话中没有购物车
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}  # 设置一个空的购物车
        self.cart = cart

    # 向购物车中添加商品
    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        product：需要在购物车中更新或者向购物车添加的 Product 对象
        quantity：一个产品数量的可选参数。默认为 1
        update_quantity：是否更新数量，这是一个布尔值
        """
        product_id = str(product.id)
        if product_id not in self.cart:   # 产品不在购物车中
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity  # 原来的数量再加后面添加的数量
        self.save()   # 把购物车保存到会话中。

    # 更新购物车物品的数量
    def update_quantity(self, product, quantity):
        """
        Add a product to the cart or update its quantity.
        product：需要在购物车中更新或者向购物车添加的 Product 对象
        quantity：产品数量
        """
        product_id = str(product.id)
        if product_id not in self.cart:   # 产品不在购物车中
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        else:
            self.cart[product_id]['quantity'] = quantity
        self.save()   # 把购物车保存到会话中。

    # 把购物车保存到会话中。
    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    # 删除购物车的产品
    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # 迭代购物车当中的物品
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()   # 产品的所有id
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)   # 取得产品的数据
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():   # id中的值
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']     # 产品的总价
            yield item

    # 返回购物车中物品的总数量。
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    # 计算购物车中物品的总价
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # 清空购物
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

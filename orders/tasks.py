from celery import task
# from django.core.mail import send_mail
from .models import Order, OrderItem
from login.models import Profile

# todo 获取用户信息，发给用户微信

# 异步任务来发送消息邮件来让用户知道他们下单了。
# task 装饰器来定义我们的 order_created 任务
# @task
# def order_created(order_id):
#     """
#     Task to send an e-mail notification when an order is
#     successfully created.
#     """
#     order = Order.objects.get(id=order_id)
#     subject = 'Order nr. {}'.format(order.id)
#     message = 'Dear {},\n\nYou have successfully placed an order.\
#                 Your order id is {}.'.format(order.first_name,
#                                             order.id)
#     # 我们使用 Django 提供的 send_mail() 函数来发送一封提示邮件给用户告诉他们下
#     mail_sent = send_mail(subject,
#                         message,
#                         'admin@myshop.com',
#                         [order.email])
#     return mail_sent


from .wechartAPI.api.src import sendmsg


@task
def order_created(order_id):
    """
    发送微信消息
    """
    order = Order.objects.get(id=order_id)
    orderitems = OrderItem.objects.filter(order=order)
    order_detail = ''
    for order_item in orderitems:
        order_detail = order_detail + str(order_item.product.name) + ':' + str(order_item.quantity) + "件。共" + str(
            order_item.get_cost()) + "元\n"
    message = '亲 {},你已经成功下单了。\n订单号{}，\n下单时间:\n {}，\n\n{}\n总金额{}元'.format(order.user.first_name, order.id,
                                                                            order.created.strftime("%Y-%m-%d %H:%M:%S"),
                                                                            order_detail,
                                                                            order.total_cost)
    # print(message)
    # 我们使用 Django 提供的 send_mail() 函数来发送一封提示邮件给用户告诉他们下
    # mail_sent = send_mail(subject,
    #                     message,
    #                     'admin@myshop.com',
    #                     [order.email])
    msg_sent = sendmsg.sendmsgbywechart(message)
    return msg_sent

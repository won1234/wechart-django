from celery import task, shared_task
# from django.core.mail import send_mail
from .models import Order, OrderItem, OrderStatistics
# from mall.models import Product
from login.models import Profile
# from datetime import date
from .wechartAPI.api.src import sendmsg


# 计划任务
# @shared_task
# def stat_orders_today():
#     # 1.取得当天的订单数据，2.对订单数据进行统计，3.通过微信发送数据，4.写入数据库，日期，产品，数量，金额
#     total = {}  # {product:{'quantity':..,'Amount':..},...}
#     msg = ''
#     today = date.today()
#     orders = Order.objects.filter(created__date=today)
#     products = Product.objects.all()
#     for product in products:  # 每样产品的数量全置为0
#         total[product] = {'quantity': 0, 'amount': 0}
#     for order in orders:  # 进行循环统计
#         order_items = OrderItem.objects.filter(order=order)
#         for order_item in order_items:
#             product = order_item.product
#             quantity = total[product]['quantity'] + order_item.quantity
#             amount = total[product]['amount'] + order_item.quantity * order_item.price
#             total[product] = {'quantity': quantity, 'amount': amount}
#     for product, qa_dic in total.items():
#         # 写入数据库,发送消息
#         quantity = qa_dic['quantity']
#         if quantity:
#             order_statistics = OrderStatistics.objects.create(date=today, product=product, quantity=quantity,
#                                                              amount=qa_dic['amount'])
#             # print(order_statistics)
#             msg = msg + product.name + ' ： ' + str(quantity) + '\n'
#     msg = today.strftime('%Y-%m-%d') + '提交的订单统计\n' + msg
#     sendmsg.test(msg)
#     return order_statistics


@task
def order_created(user_profile_id, order_id):
    """
    发送微信消息
    """
    user_profile = Profile.objects.get(id=user_profile_id)
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    first_name = user_profile.user.first_name
    order_id = order.id
    created_time = order.created.strftime("%Y-%m-%d %H:%M:%S")
    order_description = order.description
    order_detail_cost = ''
    order_detail = ''
    for order_item in order_items:
        order_detail_cost = order_detail_cost + str(order_item.product.name) + ':' + str(
            order_item.quantity) + "件。共" + str(
            order_item.get_cost()) + "元\n"
        order_detail = order_detail + str(order_item.product.name) + ':' + str(order_item.quantity) + "件。\n"
    if order_description:  # 判断有无订单描述
        message_user = '亲 {},你已经成功下单了。\n订单号{}，\n下单时间:\n {}，\n订单描述:\n {}，\n\n{}\n总金额{}元'.format(first_name,
                                                                                               order_id,
                                                                                               created_time,
                                                                                               order_description,
                                                                                               order_detail_cost,
                                                                                               order.get_total_cost())
        message_tag = '{}\n订单号{}，\n下单时间:\n {}，\n订单描述:\n {}，\n\n{}'.format(first_name,
                                                                          order_id,
                                                                          created_time,
                                                                          order_description,
                                                                          order_detail)
    else:
        message_user = '亲 {},你已经成功下单了。\n订单号{}，\n下单时间:\n {}，\n\n{}\n总金额{}元'.format(first_name,
                                                                                  order_id,
                                                                                  created_time,
                                                                                  order_detail_cost,
                                                                                  order.get_total_cost())
        message_tag = '{}\n订单号{}，\n下单时间:\n {}，\n\n{}'.format(first_name,
                                                             order_id,
                                                             created_time,
                                                             order_detail)

    msg_sent = sendmsg.sendmsgbywechart(user_profile, message_user, message_tag)
    return msg_sent

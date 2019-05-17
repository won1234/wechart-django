from celery import task
# from django.core.mail import send_mail
from .models import Order, OrderItem
from login.models import Profile

from .wechartAPI.api.src import sendmsg


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
    order_detail_cost = ''
    order_detail = ''
    for order_item in order_items:
        order_detail_cost = order_detail_cost + str(order_item.product.name) + ':' + str(
            order_item.quantity) + "件。共" + str(
            order_item.get_cost()) + "元\n"
        order_detail = order_detail + str(order_item.product.name) + ':' + str(order_item.quantity) + "件。\n"
    message_user = '亲 {},你已经成功下单了。\n订单号{}，\n下单时间:\n {}，\n\n{}\n总金额{}元'.format(first_name,
                                                                              order_id,
                                                                              created_time,
                                                                              order_detail_cost,
                                                                              order.total_cost)
    message_tag = '{}\n订单号{}，\n下单时间:\n {}，\n\n{}'.format(first_name,
                                                         order_id,
                                                         created_time,
                                                         order_detail)

    msg_sent = sendmsg.sendmsgbywechart(user_profile, message_user, message_tag)
    return msg_sent

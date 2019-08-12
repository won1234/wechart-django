from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('order_list_cost', views.order_list_cost, name='order_list_cost'),
    path('orders_today', views.orders_today, name='orders_today'),
    path('shop_statistical_table', views.shop_statistical_table, name='shop_statistical_table'),
]

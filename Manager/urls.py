from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('order_list_cost', views.order_list_cost, name='order_list_cost'),
    path('orders_today', views.orders_today, name='orders_today'),
    path('shop_statistical_table', views.shop_statistical_table, name='shop_statistical_table'),
    path('shop_shopping', views.shop_shopping, name='shop_shopping'),
    path('product_sales', views.product_sales, name='product_sales'),
    path('confirm_shipment', views.confirm_shipment, name='confirm_shipment'),
    path('confirm_paid/<int:id>/', views.confirm_paid, name='confirm_paid'),
]

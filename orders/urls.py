from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('order_created/<order_id>/', views.order_created_view, name='order_created'),
    path('order_list/', views.order_list, name='order_list'),
    path('admin_create_order/', views.admin_create_order, name='admin_create_order'),
]

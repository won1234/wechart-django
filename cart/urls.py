from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('update_quantity/<int:product_id>/', views.cart_update_quantity, name='cart_update_quantity'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]

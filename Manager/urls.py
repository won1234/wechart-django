from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('export', views.export_to_csv, name='export_list'),
]

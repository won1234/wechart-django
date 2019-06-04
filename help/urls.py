from django.urls import path
from . import views

app_name = 'help'
urlpatterns = [
            path('', views.help_list, name='help_list'),
            path('<int:id>/', views.help_detail, name='help_detail'),
]
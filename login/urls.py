from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # post views
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('', views.dashboard, name='dashboard'),
    path('change_password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]
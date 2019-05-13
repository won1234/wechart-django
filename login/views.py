from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse  # 渲染页面，重定向网页
from django.contrib.auth import authenticate, login, logout  # django的认证框架
from .forms import LoginForm   # 导入自建的forms.py中的LoginForm类


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)   # 提交的数据实例化表单（form）
        if form.is_valid():     # 检查这个表单是否有效
            cd = form.cleaned_data    # 取得数据
            # 使用authenticate()方法通过数据库对这个用户进行认证（authentication）
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:  # 如果用户存在
                if user.is_active:  # 如果用户的状态是active
                    login(request, user)  # 调用login()方法集合用户到会话（session）
                    # return HttpResponse('Authenticated successfully')
                    # print(dir(request.user))
                    return redirect(reverse('mall:product_list'))  # 重定向网页，到mall
                else:
                    return render(request, 'registrtion/login.html', {'form': form})
            else:
                return render(request, 'registrtion/login.html', {'form': form})
    else:
        form = LoginForm()     # 为GET时，传入LoginForm为空
    return render(request, 'registrtion/login.html', {'form': form})    # 无论如何最终都要返回


def user_logout(request):
    logout(request)
    return HttpResponse('登出成功！')

# @login_required             # 登录后才能执行下面的函数，默认跳转到的url为/accounts/login
# def dashboard(request):
#     return render(request,
#                  'account/dashboard.html',
#                  {'section': 'dashboard'})

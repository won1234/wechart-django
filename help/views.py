from django.shortcuts import render
from django.http import HttpResponse
from .models import Help


# Create your views here.


def help_list(request):
    # todo 1.取得文章的排序序号，标题，id,传给模版
    # 模版根据序号进行展示。
    help_docs = Help.objects.all()
    return render(request, 'help/help_list.html', {'help_docs': help_docs})

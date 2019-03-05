from django.shortcuts import render
from django.http import HttpResponse
from complaint.models import Cs
# Create your views here.

def index(request):
    return render(request, 'complaint_index.html')

def cs(request):
    cs_name = request.GET['name']
    cs_phone = request.GET['phone']
    c_or_s = request.GET['cs']
    cs_content = request.GET['content']
    Cs.objects.create(name=cs_name, phone=cs_phone, c_or_s=c_or_s, content=cs_content)
    if c_or_s == "complaint":
        return HttpResponse('您的投诉已经提交成功！我们会核对您提交的投诉后，尽快和您联系。')
    elif c_or_s == "suggest":
        return HttpResponse('您的建议已经提交成功！非常感谢您提交的建议，我们会认真考虑。')

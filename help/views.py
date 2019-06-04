from django.shortcuts import render, get_object_or_404
from .models import Help


# Create your views here.


def help_list(request):
    help_docs = Help.objects.filter(available=True)
    return render(request, 'help/help_list.html', {'help_docs': help_docs})


def help_detail(request, id):
    help_doc = get_object_or_404(Help,
                                 id=id,
                                 available=True)
    return render(request, 'help/help_detail.html', {'help_doc': help_doc})

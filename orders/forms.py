from django import forms
from .models import Order
from login.models import Profile

# USERS = Profile.objects.filter(department =)  # 取得金华配送用户
USERS = Profile.objects.all()
USERS_list = []
for i in USERS:  # 取得所有用户，形成[(id, name), ...] 元组加列表的样式
    user = i.user
    USERS_list.append((i.id, user.first_name))


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user']


class AdminCreateOrder(forms.Form):
    user = forms.TypedChoiceField(
        choices=USERS_list,
        label='用户',
        coerce=int)
    order = forms.CharField(required=True, label='订单内容', widget=forms.Textarea)

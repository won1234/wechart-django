from django import forms
from login.models import Profile

USERS = Profile.objects.all()  # 取得所有用户
USERS_list = [(0, '全部')]  # 当POST为0时，代表全部用户
# USERS_list = []  # 当POST为0时，代表全部用户
for i in USERS:
    USERS_list.append((i.user.id, i.user.first_name))
# print(USERS_list)
is_paid = ((0, '全部'), (1, '已支付'), (2, '未支付'))
is_send = ((0, '全部'), (1, '已发货'), (2, '未发货'))


class SelectOrdersForm(forms.Form):
    user = forms.TypedChoiceField(
        choices=USERS_list,
        label='用户',
        coerce=int)
    paid = forms.TypedChoiceField(choices=is_paid, label='是否支付', coerce=int)  # 是否支付
    send = forms.TypedChoiceField(choices=is_send, label='是否发货', coerce=int)  # 是否发货
    created_start = forms.DateField(required=False, label='开始日期',
                                    widget=forms.SelectDateWidget(empty_label=("年", "月", "日"))
                                    )  # 下单日期
    created_end = forms.DateField(required=False, label='结束日期',
                                  widget=forms.SelectDateWidget(empty_label=("年", "月", "日"))
                                  )  # 下单日期

from django import forms
from login.models import Profile
from mall.models import Product


# USERS = Profile.objects.all()  # 取得所有用户
# USERS_list = [(0, '全部')]  # 当POST为0时，代表全部用户
# # USERS_list = []  # 当POST为0时，代表全部用户
# for i in USERS:
#     USERS_list.append((i.user.id, i.user.first_name))
# # print(USERS_list)
# is_paid = ((0, '全部'), (1, '已支付'), (2, '未支付'))
# is_send = ((0, '全部'), (1, '已发货'), (2, '未发货'))


class SelectUserForm(forms.Form):
    user = forms.TypedChoiceField(
        # choices=USERS_list,
        label='用户',
        coerce=int)

    def __init__(self, *args, **kwargs):
        super(SelectOrdersForm, self).__init__(*args, **kwargs)
        users_list = [(0, '全部')]  # 当POST为0时，代表全部用户
        users = Profile.objects.all()  # 取得所有用户
        for i in users:
            users_list.append((i.user.id, i.user.first_name))
        self.fields['user'].choices = users_list


class SelectOrdersForm(forms.Form):
    user = forms.TypedChoiceField(
        # choices=USERS_list,
        label='用户',
        coerce=int)
    send = forms.TypedChoiceField(choices=((0, '全部'), (1, '已发货'), (2, '未发货')), label='是否发货', coerce=int)  # 是否发货
    paid = forms.TypedChoiceField(choices=((0, '全部'), (1, '已支付'), (2, '未支付')), label='是否支付', coerce=int)  # 是否支付
    # created_start = forms.DateField(required=False, label='开始日期',
    #                                 widget=forms.SelectDateWidget(empty_label=("年", "月", "日"))
    #                                 )  # 下单日期
    created_start = forms.DateField(required=False, label='开始日期',
                                    widget=forms.SelectDateWidget(years=(2019, 2020, 2021), empty_label=("年", "月", "日"))
                                    )  # 下单日期
    created_end = forms.DateField(required=False, label='结束日期',
                                  widget=forms.SelectDateWidget(years=(2019, 2020, 2021), empty_label=("年", "月", "日"))
                                  )  # 下单日期
    export_csv = forms.BooleanField(required=True, initial='off', widget=forms.HiddenInput(), label='导出cvs')

    def __init__(self, *args, **kwargs):
        super(SelectOrdersForm, self).__init__(*args, **kwargs)
        users_list = [(0, '全部')]  # 当POST为0时，代表全部用户
        users = Profile.objects.all()  # 取得所有用户
        for i in users:
            users_list.append((i.user.id, i.user.first_name))
        self.fields['user'].choices = users_list


class SelectProductsForm(forms.Form):
    product = forms.TypedChoiceField(
        label='产品',
        coerce=int)
    created_start = forms.DateField(required=False, label='开始日期',
                                    widget=forms.SelectDateWidget(empty_label=("年", "月", "日"))
                                    )  # 下单日期
    created_end = forms.DateField(required=False, label='结束日期',
                                  widget=forms.SelectDateWidget(empty_label=("年", "月", "日"))
                                  )  # 下单日期
    export_csv = forms.BooleanField(required=True, initial='off', widget=forms.HiddenInput(), label='导出cvs')

    def __init__(self, *args, **kwargs):
        super(SelectProductsForm, self).__init__(*args, **kwargs)
        products_list = [(0, '全部')]
        products = Product.objects.all()
        for i in products:
            products_list.append((i.id, i.name))
        self.fields['product'].choices = products_list

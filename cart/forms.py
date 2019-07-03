from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]  # 在 1~20 之间选择产品的数量


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        label='数量',
        coerce=int)  # coerce=int 的 TypeChoiceField 字段来把输入转换为整数
    # 展示数量是否要被加进当前的产品数量上
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class CartProductQuantityForm(forms.Form):
    # form不能使用Decimal数据类型，否则会报上面的错误，Object of type 'Decimal' is not JSON serializable
    quantity = forms.IntegerField(required=True, label='数量', min_value=0, max_value=999)


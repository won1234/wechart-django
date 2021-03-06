from django import template

register = template.Library()  # 固定格式


# get(...)
#  |      D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
#  |	键k，如果在D中，返回k对应的值，如果k不在字典D中，返回自定义的d，d默认为None
@register.filter(name='get_value')  # 注册自定义的filter
def get_value(d, key_name):  # 传入一个列表和字典。根据列表内容取得字典, 如果没有返回0
    return d.get(key_name, 0)


@register.filter(name='get_value_dic')  # 注册自定义的filter
def get_value_dic(d, key_name):  # 传入一个列表和字典。根据列表内容取得字典, 如果没有返回空字典
    return d.get(key_name, {})


# 传入两个数,返回相乘的结果
@register.filter
def multiplication(m1, m2):
    return m1 * m2


@register.filter(name='get_list_value')  # 注册自定义的filter
def get_list_value(l, index):  # 传入一个列表和数字，返回列表的这个内容，没有返回None
    try:
        res = l[index]
    except Exception:
        res = None
    finally:
        return res



# wechart-django
用于微信服务号

### 2019年7月4日
1.增加报表导出功能，`Manager/views.py 下的 export_to_csv(request)函数`
2.新增一个网页，用于管理员查看金额页面，导出功能；`def order_list_cost`
3.优化了查询数据库和导出csv
### 2019年7月5日
1.提交订单、管理页面、微信发送、导出cvs，增加了订单描述.
2.todo新增一个页面用于展示未发货，管理员用于确认发货，添加运费，默认为0；
_3.bug手机管理页面选全部时导出为空（处理不了）_
### 2019年7月6日
1.todo 折线图展示默认最近7天的用户每样产品的购物情况，与总量的情况，添加可选时间段，导出功能
2.todo 每天定时统计发送数据
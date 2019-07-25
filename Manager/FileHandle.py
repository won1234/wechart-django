#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "WGQ"
# Email: master@liwenzhou.com
# Date: 2019/1/1
# FileHandle.py为处理excel的主函数。


import xlwt


# 设置样式,name字体， height字体大小， colour字体颜色，background_colour背景色，bold字体是否加粗
def set_style(name='Times New Roman', height=280, colour=0,
              background_colour=1, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    al = xlwt.Alignment()  # 对齐方式
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    style.alignment = al

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 字体名称  Times New Roman
    font.bold = bold  # 是否加粗  True 加粗， false 不加粗
    font.underline = False  # 下划线
    font.italic = False  # 斜体字
    font.colour_index = colour  # 字体体颜色
    font.height = height  # 字体大小。excel中的1等于这里的20
    style.font = font

    borders = xlwt.Borders()  # 边框
    borders.left = xlwt.Borders.THIN  # DASHED   虚线  NO_LINE  没有 THIN        实线
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    style.borders = borders

    pattern = xlwt.Pattern()  # 背景色
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # NO_PATTERN(无背景样式), SOLID_PATTERN（有背景样式）, or 0x00 through 0x12
    pattern.pattern_fore_colour = background_colour
    style.pattern = pattern

    return style


# 传入worksheet和shop_dates对象
def new_sheet(worksheet, shop_dates):
    shop_name = shop_dates.shop_name  # 店铺名称
    shop_materials_list = shop_dates.shop_materials_type_list  # shop_material列表
    purchases = shop_dates.purchases()
    # pur_list [{'buy_date'：buy_date, 'purchases': {'材料':数量（无为0） , .,...}, 'one_day_amount': one_day_amount}, ..]
    pur_list = purchases['pur_list']
    total_amount = purchases['total_amount']  # 总金额
    material_nums_dic = purchases['material_nums_dic']
    material_amounts_dic = purchases['material_amounts_dic']
    col = len(shop_materials_list)  # 材料列数
    row = len(pur_list)  # 天数列数

    style1 = set_style(background_colour=5, bold=True)
    style2 = set_style()
    style_bold = set_style(bold=True)

    for i in range(row):  # 设置单元格宽度
        worksheet.col(i).width = 3333

    # 第一行，合并单元格写入店铺的名称
    worksheet.write_merge(0, 0, 1, col, shop_name, style=set_style(height=440, bold=True))
    # 第二行，第一个写入“单价”
    worksheet.write(2, 0, "单价", style1)
    # 第二行和第三行，写入材料的名称和单价
    for i in range(col):
        material = shop_materials_list[i].material
        worksheet.write(1, i + 1, material.material_name, style1)
        worksheet.write(2, i + 1, "￥" + str(material.material_price), style1)
    worksheet.write(1, col + 1, "每日金额", style1)
    # 第四行开始，写入清单数据pur_list
    r = 3  # 第四行
    for pur in pur_list:
        # 第一列写入日期
        worksheet.write(r, 0, pur['buy_date'].strftime("%Y/%m/%d"), style1)
        # {'材料':purchase , .,...}  一天的清单
        material_purchase_dic = pur['purchases']
        c = 1  # 列数,从第二列开始写入数量
        for shop_material in shop_materials_list:
            buy_amount = material_purchase_dic[shop_material.material]
            if buy_amount:
                worksheet.write(r, c, buy_amount, style_bold)
            else:
                worksheet.write(r, c, buy_amount, style2)
            c = c + 1
        # 最后列，每日金额
        worksheet.write(r, c, "￥" + str(pur['one_day_amount']), style1)
        r = r + 1
    # 每种材料的数量和金额
    worksheet.write(row + 3, 0, "总数量", style1)
    worksheet.write(row + 4, 0, "金额", style1)
    c = 1  # 第二列开始
    for shop_material in shop_materials_list:
        material_num = material_nums_dic[shop_material.material]
        material_amount = material_amounts_dic[shop_material.material]
        worksheet.write(row + 3, c, material_num, style1)
        worksheet.write(row + 4, c, "￥" + str(material_amount), style1)
        c = c + 1
    # 总金额
    worksheet.write(row + 5, 0, "总金额", style=set_style(height=440, bold=True))
    worksheet.write_merge(row + 5, row + 5, 1, 5, "￥" + str(total_amount), style=set_style(height=440, bold=True))


# 给表中写入内容
# 传入表,表的抬头，表内容
def add_sheet_content(worksheet, title, contents):
    col = len(contents)  # 表格的列数
    # row = len(contents[0])
    for i in range(col):  # 设置单元格宽度
        worksheet.col(i).width = 3333
    style_strong = set_style(background_colour=5, bold=True)  # 单元格样式
    style_nomal = set_style()
    style_light = set_style(colour=22)
    # 第一行，合并单元格写入标题
    worksheet.write_merge(0, 0, 0, col - 1, title, style=set_style(height=440, bold=True))
    # 写入内容
    col_i = 0
    for col_cont in contents:
        row_i = 1
        for content in col_cont:
            worksheet.write(row_i, col_i, content, style_strong)
            row_i = row_i + 1
        col_i = col_i + 1


# cont = [
#     ['产品', '单价', '2019/06/16', '2019/06/17'],
#     ['肉', '￥9.50', '82', '75'],
#     ['干菜', '￥10.00', '2', '0', '']
# ]
# workbook = xlwt.Workbook(encoding="ascii")  # 生成一个Excel文件
# worksheet = workbook.add_sheet('test')  # 创建一张sheet
# add_sheet_content(worksheet, 'Title', cont)
# workbook.save('./workbook.xls')  # 存储这个Excel文件

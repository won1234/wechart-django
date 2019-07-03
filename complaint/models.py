from django.db import models

# Create your models here.
class Cs(models.Model):
    sub_date = models.DateTimeField('提交时间', auto_now_add=True)
    name = models.CharField('姓名', max_length=20, null=True)
    phone = models.CharField('手机号', max_length=11)
    c_or_s = models.CharField('投诉建议', max_length=20)
    content = models.TextField('内容', max_length=250)
    is_process = models.BooleanField('是否处理', default=False)
    process_result = models.TextField('处理结果', max_length=250, default="")

    def property_content(self):
        return self.content[:20]
    property_content.short_description = '内容'  # 修改列的名称

    def property_process_result(self):
        return self.process_result[:20]
    property_process_result.short_description = '处理结果'

    short_content = property(property_content)
    short_process_result = property(property_process_result)


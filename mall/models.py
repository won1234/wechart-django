from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = '品类'

    def __str__(self):
        return self.name

    # 取得类目的网址
    def get_absolute_url(self):
        return reverse('mall:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='products')
    name = models.CharField(max_length=200, db_index=True)  # 名称
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='默认价格')
    stock = models.PositiveIntegerField(verbose_name='库存')             # 正整数
    available = models.BooleanField(default=True, verbose_name='状态')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'product'
        verbose_name_plural = '产品'

    def __str__(self):
        return self.name

    # 返回product_detail的url 参数为args=[self.id, self.slug]
    def get_absolute_url(self):
        return reverse('mall:product_detail',
                       args=[self.id, self.slug])


# 产品的价格组
class ProductPriceGroup(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'PriceGroup'
        verbose_name_plural = '价格组'

    def __str__(self):
        return self.name


# 给产品增加另外一个价格
class ProductPrice(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='product_price',
                                verbose_name='产品')
    price2 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    price_group = models.ForeignKey(ProductPriceGroup, null=True, on_delete=models.SET_NULL,
                                    related_name='product_price',
                                    verbose_name='价格组')

    class Meta:
        ordering = ('product',)
        verbose_name = 'ProductPrice'
        verbose_name_plural = '自定义价格'

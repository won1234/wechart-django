# Generated by Django 2.1.7 on 2019-05-12 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_profile_price_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='price_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='price_group', to='mall.ProductPriceGroup', verbose_name='价格组'),
        ),
    ]

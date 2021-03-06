# Generated by Django 2.1.7 on 2019-05-14 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20190514_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nopaydate',
            name='days',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='天数'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='group2',
            field=models.ManyToManyField(related_name='group2', to='login.Group2', verbose_name='权限'),
        ),
    ]

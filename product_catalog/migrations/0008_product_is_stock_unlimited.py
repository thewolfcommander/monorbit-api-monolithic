# Generated by Django 3.1 on 2021-02-04 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_catalog', '0007_auto_20210126_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_stock_unlimited',
            field=models.BooleanField(blank=True, default=False, help_text='Is the stock is unlimited for the product', null=True),
        ),
    ]
# Generated by Django 3.1 on 2021-02-19 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_catalog', '0009_producttopping'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttopping',
            name='product',
            field=models.ForeignKey(default=1, help_text='Reference to the Product for which the topping have given', on_delete=django.db.models.deletion.CASCADE, to='product_catalog.product'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.1 on 2020-11-15 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_catalog', '0002_auto_20201012_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('change_side', models.BooleanField(default=True, help_text='If True, then the change would be positive, otherwise - negative')),
                ('price_change', models.DecimalField(decimal_places=2, default=0.0, help_text='This will be the Price Change from the Original Product Price', max_digits=12)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalog.product')),
            ],
        ),
    ]
# Generated by Django 3.1 on 2020-10-12 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0001_initial'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('day_id', models.IntegerField(blank=True, default=1, null=True)),
                ('is_billing_shipping_same', models.BooleanField(default=False)),
                ('status', models.CharField(blank=True, choices=[('Created', 'Created'), ('Confirmed', 'Confirmed'), ('Shipped', 'Shipped'), ('Dispatched', 'Dispatched'), ('Out', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned'), ('Refunded', 'Refunded')], default='Created', max_length=255, null=True)),
                ('shipping_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('billing_address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='billing_address', to='addresses.address')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shipping_address', to='addresses.address')),
            ],
        ),
    ]

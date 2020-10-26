# Generated by Django 3.1 on 2020-10-25 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Created', 'Created'), ('Confirmed', 'Confirmed'), ('Shipped', 'Shipped'), ('Dispatched', 'Dispatched'), ('Out', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned'), ('Refunded', 'Refunded'), ('Archived', 'Archived')], default='Created', max_length=255, null=True),
        ),
    ]

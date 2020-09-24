# Generated by Django 3.1 on 2020-09-24 15:29

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('premium', '0016_auto_20200924_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='trial_expiry',
            field=models.DateField(default=datetime.datetime(2021, 9, 24, 15, 29, 31, 737740, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipsubscription',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2021, 9, 24, 15, 29, 31, 737740, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='NetworkMembershipInvoice',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('invoice_period_start_date', models.DateField(blank=True, null=True)),
                ('invoice_period_end_date', models.DateField(blank=True, null=True)),
                ('invoice_description', models.TextField(blank=True, null=True)),
                ('invoice_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('invoice_created', models.DateTimeField(auto_now_add=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='premium.networkmembershipsubscription')),
            ],
        ),
    ]

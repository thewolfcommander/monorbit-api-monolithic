# Generated by Django 3.1 on 2020-08-31 07:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('premium', '0009_auto_20200831_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2021, 8, 31, 7, 36, 8, 246492, tzinfo=utc)),
        ),
    ]
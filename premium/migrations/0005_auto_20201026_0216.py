# Generated by Django 3.1 on 2020-10-25 20:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('premium', '0004_auto_20201018_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='trial_expiry',
            field=models.DateField(default=datetime.datetime(2021, 10, 25, 20, 46, 35, 271569, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipsubscription',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2021, 10, 25, 20, 46, 35, 271569, tzinfo=utc)),
        ),
    ]

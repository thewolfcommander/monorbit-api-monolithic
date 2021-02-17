# Generated by Django 3.1 on 2021-02-14 17:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('premium', '0025_auto_20210214_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='activity_downgrade_limit',
            field=models.DateField(default=datetime.datetime(2021, 5, 15, 17, 4, 34, 169499, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='activity_upgrade_limit',
            field=models.DateField(default=datetime.datetime(2021, 5, 15, 17, 4, 34, 169499, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='trial_expiry',
            field=models.DateField(default=datetime.datetime(2022, 2, 14, 17, 4, 34, 169499, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipsubscription',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2022, 2, 14, 17, 4, 34, 169499, tzinfo=utc)),
        ),
    ]

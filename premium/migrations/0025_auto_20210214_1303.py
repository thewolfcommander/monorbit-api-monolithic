# Generated by Django 3.1 on 2021-02-14 07:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('premium', '0024_auto_20210204_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='activity_downgrade_limit',
            field=models.DateField(default=datetime.datetime(2021, 5, 15, 7, 33, 43, 690416, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='activity_upgrade_limit',
            field=models.DateField(default=datetime.datetime(2021, 5, 15, 7, 33, 43, 690416, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='trial_expiry',
            field=models.DateField(default=datetime.datetime(2022, 2, 14, 7, 33, 43, 690416, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipsubscription',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2022, 2, 14, 7, 33, 43, 690416, tzinfo=utc)),
        ),
    ]

# Generated by Django 3.1 on 2020-12-13 08:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('premium', '0019_auto_20201209_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='activity_downgrade_limit',
            field=models.DateField(default=datetime.datetime(2021, 3, 13, 8, 38, 44, 705361, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='activity_upgrade_limit',
            field=models.DateField(default=datetime.datetime(2021, 3, 13, 8, 38, 44, 705361, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='trial_expiry',
            field=models.DateField(default=datetime.datetime(2021, 12, 13, 8, 38, 44, 705361, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipsubscription',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2021, 12, 13, 8, 38, 44, 705361, tzinfo=utc)),
        ),
    ]

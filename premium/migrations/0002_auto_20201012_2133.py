# Generated by Django 3.1 on 2020-10-12 16:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('premium', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='trial_expiry',
            field=models.DateField(default=datetime.datetime(2021, 10, 12, 16, 3, 1, 347311, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipsubscription',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2021, 10, 12, 16, 3, 1, 347311, tzinfo=utc)),
        ),
    ]

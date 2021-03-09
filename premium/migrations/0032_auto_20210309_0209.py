# Generated by Django 3.1 on 2021-03-08 20:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('premium', '0031_auto_20210220_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='activity_downgrade_limit',
            field=models.DateField(default=datetime.datetime(2021, 6, 6, 20, 39, 13, 527579, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='activity_upgrade_limit',
            field=models.DateField(default=datetime.datetime(2021, 6, 6, 20, 39, 13, 527579, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='trial_expiry',
            field=models.DateField(default=datetime.datetime(2022, 3, 8, 20, 39, 13, 527579, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipsubscription',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2022, 3, 8, 20, 39, 13, 527579, tzinfo=utc)),
        ),
    ]
# Generated by Django 3.1 on 2021-02-19 08:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('premium', '0028_auto_20210219_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='activity_downgrade_limit',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 8, 3, 53, 361679, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='activity_upgrade_limit',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 8, 3, 53, 361679, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipactivity',
            name='trial_expiry',
            field=models.DateField(default=datetime.datetime(2022, 2, 19, 8, 3, 53, 361679, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='networkmembershipsubscription',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2022, 2, 19, 8, 3, 53, 361679, tzinfo=utc)),
        ),
    ]

# Generated by Django 3.1 on 2020-11-16 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20201012_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='network',
            name='is_premium',
        ),
        migrations.AddField(
            model_name='network',
            name='is_basic',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='network',
            name='is_economy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='network',
            name='is_elite',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.1 on 2020-08-27 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 3.1 on 2020-10-01 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20200901_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='alt_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

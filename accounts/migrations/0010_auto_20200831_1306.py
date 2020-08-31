# Generated by Django 3.1 on 2020-08-31 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200818_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailverifyotp',
            name='expiry',
        ),
        migrations.RemoveField(
            model_name='passwordresettoken',
            name='expiry',
        ),
        migrations.AlterField(
            model_name='emailverifyotp',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='passwordresettoken',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

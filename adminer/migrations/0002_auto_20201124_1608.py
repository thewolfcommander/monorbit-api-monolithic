# Generated by Django 3.1 on 2020-11-24 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactus',
            old_name='email_or_phone',
            new_name='phone',
        ),
        migrations.AddField(
            model_name='contactus',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
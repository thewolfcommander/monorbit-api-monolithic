# Generated by Django 3.1 on 2020-11-16 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.CharField(blank=True, max_length=25, primary_key=True, serialize=False, unique=True)),
                ('email_or_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('lat', models.CharField(blank=True, max_length=50, null=True)),
                ('lng', models.CharField(blank=True, max_length=50, null=True)),
                ('is_email', models.BooleanField(default=False)),
                ('is_phone', models.BooleanField(default=False)),
                ('is_contacted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

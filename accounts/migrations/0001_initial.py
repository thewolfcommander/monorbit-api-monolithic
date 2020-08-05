# Generated by Django 3.1 on 2020-08-05 12:12

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import monorbit.utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('hash_token', models.CharField(blank=True, max_length=255, null=True)),
                ('full_name', models.CharField(blank=True, help_text='This will be the user full name', max_length=255, null=True, verbose_name='full_name')),
                ('email', models.EmailField(blank=True, error_messages={'required': 'Please provide your email address.', 'unique': 'An account with this email exist.'}, help_text='This will be the user email', max_length=255, null=True, validators=[django.core.validators.EmailValidator, monorbit.utils.validators.custom_email_validator])),
                ('mobile_number', models.CharField(blank=True, help_text='This will be the user phone number', max_length=17, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender'), ('Custom', 'Custom')], default='Male', max_length=30, null=True)),
                ('dob', models.CharField(blank=True, default='22-01-2000', max_length=100, null=True)),
                ('registration_reference', models.CharField(blank=True, default='None', max_length=255, null=True)),
                ('is_consumer', models.BooleanField(default=True, help_text='This will determine whether the user is a consumer')),
                ('is_creator', models.BooleanField(default=False, help_text='This will determine whether the user is a creator. Default it will be false')),
                ('is_working_profile', models.BooleanField(default=False, help_text='This will determine whether the user has a working profile. Default it will be false')),
                ('is_active', models.BooleanField(default=True, help_text='This will determine whether the user accound is active or not')),
                ('is_agreed_to_terms', models.BooleanField(default=True, help_text='This will determine whether the user is agreed to terms or not')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_mobile_verified', models.BooleanField(default=False, help_text='This will determine whether the mobile number is verified or not')),
                ('is_email_verified', models.BooleanField(default=False, help_text='This will determine whether the email address is verified or not')),
                ('is_logged_in', models.BooleanField(default=False)),
                ('is_archived', models.BooleanField(default=False)),
                ('registered_on', models.DateTimeField(default=django.utils.timezone.now, help_text='This will determine when the user registered')),
                ('last_logged_in_time', models.DateTimeField(default=django.utils.timezone.now, help_text='This will determine when the user registered')),
                ('updated_on', models.DateTimeField(auto_now=True, help_text='This will determine when the user updated')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

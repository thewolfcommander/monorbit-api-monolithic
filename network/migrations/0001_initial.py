# Generated by Django 3.1 on 2020-10-09 20:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('urlid', models.CharField(blank=True, max_length=255, unique=True)),
                ('network_url', models.URLField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('thumbnail_image', models.URLField(blank=True, default='https://content.monorbit.com/images/placeholder.png', null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('landmark', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('alt_phone', models.CharField(blank=True, help_text='This will be the Alternative phone number', max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('alt_email', models.EmailField(blank=True, help_text='This will be the alternative email', max_length=255, null=True, validators=[django.core.validators.EmailValidator])),
                ('rating', models.DecimalField(decimal_places=1, default=5.0, max_digits=2)),
                ('no_of_reviews', models.IntegerField(blank=True, default=0, null=True)),
                ('registered_stores', models.IntegerField(blank=True, default=1, null=True)),
                ('followers', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('gst', models.CharField(blank=True, max_length=255, null=True)),
                ('adhaar', models.CharField(blank=True, max_length=255, null=True)),
                ('pan', models.CharField(blank=True, max_length=255, null=True)),
                ('is_verified', models.BooleanField(default=False, help_text='This is for verification of uploaded documents')),
                ('is_active', models.BooleanField(default=True)),
                ('is_premium', models.BooleanField(default=False)),
                ('is_archived', models.BooleanField(default=False)),
                ('is_spam', models.BooleanField(default=False)),
                ('is_video', models.BooleanField(default=False)),
                ('is_document', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NetworkCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('priority', models.IntegerField(blank=True, default=2, null=True)),
                ('image', models.URLField(blank=True, default='https://content.monorbit.com/images/placeholder.png', null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='NetworkJob',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('job_name', models.CharField(blank=True, max_length=255, null=True)),
                ('job_type', models.CharField(blank=True, choices=[('freelancer', 'Freelancer'), ('delivery', 'Delivery'), ('permanent', 'Permanent')], default='permanent', max_length=255, null=True)),
                ('job_description', models.TextField(blank=True, null=True)),
                ('job_requirements', models.TextField(blank=True, null=True)),
                ('salary_payout_type', models.CharField(blank=True, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('bimonthly', 'Bi Monthly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('biyearly', 'Bi Yearly'), ('yearly', 'Yearly'), ('work', 'Work Basis')], default='monthly', max_length=255, null=True)),
                ('salary_lower_range', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('salary_upper_range', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('actual_salary', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('age_bar_upper', models.IntegerField(blank=True, default=45, null=True)),
                ('age_bar_lower', models.IntegerField(blank=True, default=18, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_spam', models.BooleanField(default=False)),
                ('is_vacant', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.network')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.URLField(blank=True, default='https://content.monorbit.com/images/placeholder.png', null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='NetworkVideo',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('video', models.URLField(blank=True, null=True)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.network')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkStaff',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('application_id', models.CharField(blank=True, max_length=20, null=True)),
                ('promoted_count', models.IntegerField(default=0)),
                ('demoted_count', models.IntegerField(default=0)),
                ('employee_score', models.IntegerField(default=10, help_text='This score would be given to employee out of 10.')),
                ('is_active', models.BooleanField(default=True)),
                ('joined', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.networkjob')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_profiles.jobprofile')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkReview',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('rating', models.DecimalField(decimal_places=1, default=5.0, max_digits=2)),
                ('comment', models.TextField(blank=True, null=True)),
                ('is_spam', models.BooleanField(default=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.network')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkOperationTiming',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('day', models.CharField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday'), ('All', 'All'), ('Weekday', 'Weekday'), ('Weekend', 'Weekend')], default='All', max_length=255, null=True)),
                ('opening', models.CharField(blank=True, max_length=25, null=True)),
                ('status', models.BooleanField(default=True)),
                ('closing', models.CharField(blank=True, max_length=25, null=True)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.network')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkOperationLocation',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.network')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkJobOffering',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('offering_information', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_filled', models.BooleanField(default=False)),
                ('max_staff_for_job', models.IntegerField(blank=True, default=5, null=True)),
                ('last_date', models.DateField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.networkjob')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkImage',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.network')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkDocument',
            fields=[
                ('id', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('doc', models.URLField(blank=True, null=True)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.network')),
            ],
        ),
        migrations.AddField(
            model_name='network',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='network.networkcategory'),
        ),
        migrations.AddField(
            model_name='network',
            name='network_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='network.networktype'),
        ),
        migrations.AddField(
            model_name='network',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 3.1 on 2020-08-23 18:49

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import monorbit.utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonInfo',
            fields=[
                ('id', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('is_recharged', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryBoy',
            fields=[
                ('commoninfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='job_profiles.commoninfo')),
                ('short_bio', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Delivery Boy Profile',
                'verbose_name_plural': 'Delivery Boy Profiles',
            },
            bases=('job_profiles.commoninfo',),
        ),
        migrations.CreateModel(
            name='Freelancer',
            fields=[
                ('commoninfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='job_profiles.commoninfo')),
                ('short_bio', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Freelancer Profile',
                'verbose_name_plural': 'Freelancer Profiles',
            },
            bases=('job_profiles.commoninfo',),
        ),
        migrations.CreateModel(
            name='PermanentEmployee',
            fields=[
                ('commoninfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='job_profiles.commoninfo')),
                ('short_bio', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Permanent Employee Profile',
                'verbose_name_plural': 'Permanent Employee Profiles',
            },
            bases=('job_profiles.commoninfo',),
        ),
        migrations.CreateModel(
            name='JobProfile',
            fields=[
                ('id', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('alt_email', models.EmailField(blank=True, help_text="This will be the user's alternative email", max_length=255, null=True, validators=[django.core.validators.EmailValidator, monorbit.utils.validators.custom_email_validator])),
                ('alt_phone_number', models.CharField(blank=True, help_text="This will be the user's alternative phone number", max_length=10, null=True)),
                ('photo_url', models.URLField(blank=True, help_text="This will be applier's passport size photograph", null=True)),
                ('adhaar_card', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, help_text='Address Line 1', max_length=255, null=True)),
                ('landmark', models.CharField(blank=True, help_text='Landmark', max_length=255, null=True)),
                ('city', models.CharField(blank=True, help_text='City you are living in', max_length=255, null=True)),
                ('state', models.CharField(blank=True, help_text='State you belong to', max_length=255, null=True)),
                ('country', models.CharField(blank=True, help_text='Country', max_length=255, null=True)),
                ('pincode', models.CharField(blank=True, help_text='Area POstal code', max_length=15, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_vehicle', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_delivery_boy', models.BooleanField(default=False)),
                ('is_permanent_employee', models.BooleanField(default=False)),
                ('is_freelancer', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job Profile',
                'verbose_name_plural': 'Job Profiles',
            },
        ),
        migrations.AddField(
            model_name='commoninfo',
            name='job_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_profiles.jobprofile'),
        ),
        migrations.CreateModel(
            name='PermanentEmployeeSpecification',
            fields=[
                ('id', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('spec_type', models.CharField(choices=[('skills', 'Skills'), ('link', 'Links'), ('experience', 'Experiences'), ('other', 'Other')], default='skills', max_length=50)),
                ('label', models.CharField(blank=True, help_text='Label of the Specification', max_length=255, null=True)),
                ('description', models.TextField(blank=True, help_text='Description of the Specification', null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('permanent_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_profiles.permanentemployee')),
            ],
            options={
                'verbose_name': 'Permanent Employee Specification',
                'verbose_name_plural': 'Permanent Employee Specifications',
            },
        ),
        migrations.CreateModel(
            name='PermanentEmployeeFile',
            fields=[
                ('id', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('file_type', models.CharField(choices=[('document', 'Document'), ('image', 'Image'), ('video', 'Video')], default='image', max_length=50)),
                ('label', models.CharField(blank=True, help_text='Label on the File', max_length=255, null=True)),
                ('file_url', models.URLField(blank=True, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('permanent_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_profiles.permanentemployee')),
            ],
            options={
                'verbose_name': 'Permanent Employee File',
                'verbose_name_plural': 'Permanent Employee Files',
            },
        ),
        migrations.CreateModel(
            name='FreelancerSpecification',
            fields=[
                ('id', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('spec_type', models.CharField(choices=[('skills', 'Skills'), ('link', 'Links'), ('experience', 'Experiences'), ('other', 'Other')], default='skills', max_length=50)),
                ('label', models.CharField(blank=True, help_text='Label of the Specification', max_length=255, null=True)),
                ('description', models.TextField(blank=True, help_text='Description of the Specification', null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_profiles.freelancer')),
            ],
            options={
                'verbose_name': 'Freelancer Specification',
                'verbose_name_plural': 'Freelancer Specifications',
            },
        ),
        migrations.CreateModel(
            name='FreelancerFile',
            fields=[
                ('id', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('file_type', models.CharField(choices=[('document', 'Document'), ('image', 'Image'), ('video', 'Video')], default='image', max_length=50)),
                ('label', models.CharField(blank=True, help_text='Label on the File', max_length=255, null=True)),
                ('file_url', models.URLField(blank=True, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_profiles.freelancer')),
            ],
            options={
                'verbose_name': 'Freelancer File',
                'verbose_name_plural': 'Freelancer Files',
            },
        ),
        migrations.CreateModel(
            name='DeliveryBoyVehicle',
            fields=[
                ('id', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('driving_license', models.CharField(blank=True, help_text='Driving License of the Delivery Boy', max_length=50, null=True)),
                ('type_of_vehicle', models.CharField(choices=[('bicycle', 'Bi Cycle'), ('motor_bike', 'Motor Bike'), ('car', 'Car'), ('semi_truck', 'Semi Truck'), ('other', 'Other')], default='motor_bike', max_length=255)),
                ('vehicle_license', models.CharField(blank=True, help_text='Vehicle License Number', max_length=50, null=True, unique=True)),
                ('valid_upto', models.DateField(default=datetime.date.today, help_text='Validity date of Vehicle')),
                ('vehicle_photo_url', models.URLField(blank=True, help_text='Upload Vehicle Image from front showing verhicle registration number. We will then verify the number from this image with vehicle_license field', null=True)),
                ('active', models.BooleanField(default=False)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('delivery_boy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_profiles.deliveryboy')),
            ],
            options={
                'verbose_name': 'Delivery Boy Vehicle',
                'verbose_name_plural': 'Delivery Boy Vehicles',
            },
        ),
    ]
# Generated by Django 3.1 on 2020-10-12 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryboyvehicle',
            name='vehicle_photo_url',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text='Upload Vehicle Image from front showing verhicle registration number. We will then verify the number from this image with vehicle_license field', null=True),
        ),
        migrations.AlterField(
            model_name='freelancerfile',
            name='file_url',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True),
        ),
        migrations.AlterField(
            model_name='jobprofile',
            name='photo_url',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text="This will be applier's passport size photograph", null=True),
        ),
        migrations.AlterField(
            model_name='permanentemployeefile',
            name='file_url',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True),
        ),
    ]

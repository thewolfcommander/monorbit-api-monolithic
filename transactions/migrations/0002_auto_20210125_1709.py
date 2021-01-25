# Generated by Django 3.1 on 2021-01-25 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_networktrial_expiry'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_profiles', '0002_auto_20201012_2133'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkdeliveryboyapplication',
            name='application_status',
            field=models.CharField(blank=True, choices=[('applied', 'Applied'), ('in_touch', 'In Touch'), ('hired', 'Hired'), ('fired', 'Fired'), ('rejected', 'Rejected')], default='applied', help_text='Job Application status', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='networkdeliveryboyapplication',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp at which the delivery boy applied for the job'),
        ),
        migrations.AlterField(
            model_name='networkdeliveryboyapplication',
            name='delivery_boy',
            field=models.ForeignKey(help_text='This would be the reference to the delivery boy who is applying to the job offering', on_delete=django.db.models.deletion.CASCADE, to='job_profiles.deliveryboy'),
        ),
        migrations.AlterField(
            model_name='networkdeliveryboyapplication',
            name='offering',
            field=models.ForeignKey(help_text='This would be the reference to the Network Job Offering Table. It means this application is going to made to that respective job offering by network.', on_delete=django.db.models.deletion.CASCADE, to='network.networkjoboffering'),
        ),
        migrations.AlterField(
            model_name='networkdeliveryboyapplication',
            name='updated',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp at which the application has been updated'),
        ),
        migrations.AlterField(
            model_name='networkfollower',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='The timestamp at which the user followed the network'),
        ),
        migrations.AlterField(
            model_name='networkfollower',
            name='network',
            field=models.ForeignKey(help_text='This would be the reference to the Network', on_delete=django.db.models.deletion.CASCADE, to='network.network'),
        ),
        migrations.AlterField(
            model_name='networkfollower',
            name='user',
            field=models.ForeignKey(blank=True, help_text='This would be reference to the User who is following the network', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='networkfreelancerapplication',
            name='application_status',
            field=models.CharField(blank=True, choices=[('applied', 'Applied'), ('in_touch', 'In Touch'), ('hired', 'Hired'), ('fired', 'Fired'), ('rejected', 'Rejected')], default='applied', help_text='Job Application status', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='networkfreelancerapplication',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp at which the freelancer applied for the job'),
        ),
        migrations.AlterField(
            model_name='networkfreelancerapplication',
            name='freelancer',
            field=models.ForeignKey(help_text='This would be the reference to the freelancer who is applying for the Job Offering', on_delete=django.db.models.deletion.CASCADE, to='job_profiles.freelancer'),
        ),
        migrations.AlterField(
            model_name='networkfreelancerapplication',
            name='offering',
            field=models.ForeignKey(help_text='This would be the reference to the Network Job Offering Table. It means this application is going to made to that respective job offering by network.', on_delete=django.db.models.deletion.CASCADE, to='network.networkjoboffering'),
        ),
        migrations.AlterField(
            model_name='networkfreelancerapplication',
            name='updated',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp at which the application has been updated'),
        ),
        migrations.AlterField(
            model_name='networkpermanentemployeeapplication',
            name='application_status',
            field=models.CharField(blank=True, choices=[('applied', 'Applied'), ('in_touch', 'In Touch'), ('hired', 'Hired'), ('fired', 'Fired'), ('rejected', 'Rejected')], default='applied', help_text='Job Application status', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='networkpermanentemployeeapplication',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp at which the permanent employee applied for the job'),
        ),
        migrations.AlterField(
            model_name='networkpermanentemployeeapplication',
            name='offering',
            field=models.ForeignKey(help_text='This would be the reference to the Network Job Offering Table. It means this application is going to made to that respective job offering by network.', on_delete=django.db.models.deletion.CASCADE, to='network.networkjoboffering'),
        ),
        migrations.AlterField(
            model_name='networkpermanentemployeeapplication',
            name='permanent_employee',
            field=models.ForeignKey(help_text='This would be the reference to the permanent employee who is applying for the Job Offering', on_delete=django.db.models.deletion.CASCADE, to='job_profiles.permanentemployee'),
        ),
        migrations.AlterField(
            model_name='networkpermanentemployeeapplication',
            name='updated',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp at which the application has been updated'),
        ),
    ]

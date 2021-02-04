# Generated by Django 3.1 on 2021-02-04 10:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job_profiles', '0002_auto_20201012_2133'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('network', '0008_networktrial_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='lat',
            field=models.CharField(blank=True, default='24.67856', help_text='This is the lattitude of the network locations', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='network',
            name='lng',
            field=models.CharField(blank=True, default='76.65115', help_text='This is the longitude of the network locations', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='address',
            field=models.CharField(blank=True, help_text='Address of the network', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='adhaar',
            field=models.CharField(blank=True, help_text='Adhaar number of the network owner', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='alt_email',
            field=models.EmailField(blank=True, help_text='This will be the alternative email or the main business email', max_length=255, null=True, validators=[django.core.validators.EmailValidator]),
        ),
        migrations.AlterField(
            model_name='network',
            name='alt_phone',
            field=models.CharField(blank=True, help_text='This will be the Alternative phone number or the main business phone number', max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='network',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Reference to the Network Category to which this network instance belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='network.networkcategory'),
        ),
        migrations.AlterField(
            model_name='network',
            name='city',
            field=models.CharField(blank=True, help_text='City in which network exists primarily', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='country',
            field=models.CharField(blank=True, help_text='Country in which network exists primarily', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp at which the network has been created'),
        ),
        migrations.AlterField(
            model_name='network',
            name='followers',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='No of followers of the network, means no of users who have joined the network ', null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='gst',
            field=models.CharField(blank=True, help_text='GST Number of the network', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='id',
            field=models.CharField(blank=True, help_text='Primary key of the Network', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='is_active',
            field=models.BooleanField(default=True, help_text='If true, means network is actively working on Monorbit'),
        ),
        migrations.AlterField(
            model_name='network',
            name='is_archived',
            field=models.BooleanField(default=False, help_text='If true, it means network is archived or deleted temporarily'),
        ),
        migrations.AlterField(
            model_name='network',
            name='is_basic',
            field=models.BooleanField(default=True, help_text='If true, it means network is using basic plan currently'),
        ),
        migrations.AlterField(
            model_name='network',
            name='is_document',
            field=models.BooleanField(default=False, help_text='If true, the network have uploaded a document about the network like manual, brochure or something like that'),
        ),
        migrations.AlterField(
            model_name='network',
            name='is_economy',
            field=models.BooleanField(default=False, help_text='If true, it means network is using economy plan currently'),
        ),
        migrations.AlterField(
            model_name='network',
            name='is_elite',
            field=models.BooleanField(default=False, help_text='If true, it means network is using the elite plan currently'),
        ),
        migrations.AlterField(
            model_name='network',
            name='is_spam',
            field=models.BooleanField(default=False, help_text='If true, the network is not valid and is marked as spam or it is fake'),
        ),
        migrations.AlterField(
            model_name='network',
            name='is_video',
            field=models.BooleanField(default=False, help_text='If true, the network have uploaded display video about the network'),
        ),
        migrations.AlterField(
            model_name='network',
            name='landmark',
            field=models.CharField(blank=True, help_text='Landmark near network location', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='name',
            field=models.CharField(blank=True, help_text='Name of the Network', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='network_type',
            field=models.ForeignKey(blank=True, help_text='Reference to the Network Type to which this network instance belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='network.networktype'),
        ),
        migrations.AlterField(
            model_name='network',
            name='network_url',
            field=models.URLField(blank=True, help_text='Public Network URL', null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='no_of_reviews',
            field=models.IntegerField(blank=True, default=0, help_text='No of reviews given by the users on the network', null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='pan',
            field=models.CharField(blank=True, help_text='PAN Number of the network ownerr', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='pincode',
            field=models.CharField(blank=True, help_text='PIN code to which network location belongs to', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5.0, help_text='Overall rating of the network given by the users', max_digits=2),
        ),
        migrations.AlterField(
            model_name='network',
            name='registered_stores',
            field=models.IntegerField(blank=True, default=1, help_text='No of registered stores under a single network', null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='state',
            field=models.CharField(blank=True, help_text='State in which network exists primarily', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='thumbnail_image',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text='Logo of the network or the main display image of the network', null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp at which the network has been updated'),
        ),
        migrations.AlterField(
            model_name='network',
            name='urlid',
            field=models.CharField(blank=True, help_text='This would be the unique username of the network that the netwrk will use for better URL Accessibility', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Reference to the User who is the owner of the network', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='networkcategory',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp at which the network category is created'),
        ),
        migrations.AlterField(
            model_name='networkcategory',
            name='image',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text='Category Display image', null=True),
        ),
        migrations.AlterField(
            model_name='networkcategory',
            name='name',
            field=models.CharField(blank=True, help_text='Name of the network category', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='networkcategory',
            name='priority',
            field=models.IntegerField(blank=True, default=2, help_text='Priority of the category. Will be deprecated soon.', null=True),
        ),
        migrations.AlterField(
            model_name='networkdocument',
            name='doc',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text='Actual Document URL', null=True),
        ),
        migrations.AlterField(
            model_name='networkdocument',
            name='id',
            field=models.CharField(blank=True, help_text='Primary Key of the Network Document', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='networkdocument',
            name='label',
            field=models.CharField(blank=True, help_text='Label for the document specifying what the document depicts actually', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='networkdocument',
            name='network',
            field=models.ForeignKey(help_text='Reference to the network who is uploading the document', on_delete=django.db.models.deletion.CASCADE, to='network.network'),
        ),
        migrations.AlterField(
            model_name='networkimage',
            name='id',
            field=models.CharField(blank=True, help_text='Primary Key of the Network Image', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='networkimage',
            name='image',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text='Actual image URL', null=True),
        ),
        migrations.AlterField(
            model_name='networkimage',
            name='label',
            field=models.CharField(blank=True, help_text='Label for the image specifying what the image depicts actually', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='networkimage',
            name='network',
            field=models.ForeignKey(help_text='Reference to the Network who is uploading the image', on_delete=django.db.models.deletion.CASCADE, to='network.network'),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='actual_salary',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Actual Salary for the job', max_digits=10),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='age_bar_lower',
            field=models.IntegerField(blank=True, default=18, help_text='Minimum age limit for the job', null=True),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='age_bar_upper',
            field=models.IntegerField(blank=True, default=45, help_text='Maximum age limit for the job', null=True),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp at which the job has been created by the network'),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='id',
            field=models.CharField(blank=True, help_text='Primary Key of the network Job', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='is_active',
            field=models.BooleanField(default=True, help_text='If true, the job is currently active'),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='is_spam',
            field=models.BooleanField(default=False, help_text='If true, job is marked as spam by Monorbit'),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='is_vacant',
            field=models.BooleanField(default=True, help_text='If true, job has vacancy'),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='is_verified',
            field=models.BooleanField(default=False, help_text='If true, job is successfully verified by Monorbit'),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='job_description',
            field=models.TextField(blank=True, help_text='Description about the job', null=True),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='job_name',
            field=models.CharField(blank=True, help_text='Name of the job e.g. Receptionist', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='job_requirements',
            field=models.TextField(blank=True, help_text='Requirements for the Job', null=True),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='job_type',
            field=models.CharField(blank=True, choices=[('freelancer', 'Freelancer'), ('delivery', 'Delivery'), ('permanent', 'Permanent')], default='permanent', help_text='Type of job', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='network',
            field=models.ForeignKey(help_text='reference to the network who is creating the Job', on_delete=django.db.models.deletion.CASCADE, to='network.network'),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='salary_lower_range',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Minimum Salary for the Job', max_digits=10),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='salary_payout_type',
            field=models.CharField(blank=True, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('bimonthly', 'Bi Monthly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('biyearly', 'Bi Yearly'), ('yearly', 'Yearly'), ('work', 'Work Basis')], default='monthly', help_text='It tells how salary is going to be paid in terms of time', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='salary_upper_range',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Maximum salary for the job', max_digits=10),
        ),
        migrations.AlterField(
            model_name='networkjob',
            name='updated',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp at which the job has been updated'),
        ),
        migrations.AlterField(
            model_name='networkjoboffering',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp at which the offering created'),
        ),
        migrations.AlterField(
            model_name='networkjoboffering',
            name='id',
            field=models.CharField(blank=True, help_text='Primary Key of the Job offering', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='networkjoboffering',
            name='is_active',
            field=models.BooleanField(default=True, help_text='If true, it means the offering is active and is accepting applications'),
        ),
        migrations.AlterField(
            model_name='networkjoboffering',
            name='is_filled',
            field=models.BooleanField(default=False, help_text='If true it means the offering has been already filled'),
        ),
        migrations.AlterField(
            model_name='networkjoboffering',
            name='job',
            field=models.ForeignKey(help_text='Reference to the Job for which the offering has been created', on_delete=django.db.models.deletion.CASCADE, to='network.networkjob'),
        ),
        migrations.AlterField(
            model_name='networkjoboffering',
            name='last_date',
            field=models.DateField(default=django.utils.timezone.now, help_text='Last date to apply for the job offering'),
        ),
        migrations.AlterField(
            model_name='networkjoboffering',
            name='max_staff_for_job',
            field=models.IntegerField(blank=True, default=5, help_text='Maximum no of staff needed fro the job offering', null=True),
        ),
        migrations.AlterField(
            model_name='networkjoboffering',
            name='offering_information',
            field=models.TextField(blank=True, help_text='More informatioin about the offering like job details, perks etc.', null=True),
        ),
        migrations.AlterField(
            model_name='networkjoboffering',
            name='title',
            field=models.CharField(blank=True, help_text='Title of the Job offering', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='networkjoboffering',
            name='updated',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp at which the offering has been updated'),
        ),
        migrations.AlterField(
            model_name='networkoperationlocation',
            name='id',
            field=models.CharField(blank=True, help_text='Primary key of the location', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='networkoperationlocation',
            name='network',
            field=models.ForeignKey(help_text='Reference to the network who is addding the location', on_delete=django.db.models.deletion.CASCADE, to='network.network'),
        ),
        migrations.AlterField(
            model_name='networkoperationlocation',
            name='pincode',
            field=models.CharField(blank=True, help_text='Pincode in which the network is operational', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='networkoperationtiming',
            name='closing',
            field=models.CharField(blank=True, help_text='Closing time for the day e.g. 06:00 PM', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='networkoperationtiming',
            name='day',
            field=models.CharField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday'), ('All', 'All'), ('Weekday', 'Weekday'), ('Weekend', 'Weekend')], default='All', help_text='Day for which timing is being added', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='networkoperationtiming',
            name='id',
            field=models.CharField(blank=True, help_text='Primary Key of the timing', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='networkoperationtiming',
            name='network',
            field=models.ForeignKey(help_text='Reference to the network who is adding the timing', on_delete=django.db.models.deletion.CASCADE, to='network.network'),
        ),
        migrations.AlterField(
            model_name='networkoperationtiming',
            name='opening',
            field=models.CharField(blank=True, help_text='Opening time for the day e.g. 10:00 AM', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='networkoperationtiming',
            name='status',
            field=models.BooleanField(default=True, help_text='If true, means the network is operating for the day. False means network is closed for the day.'),
        ),
        migrations.AlterField(
            model_name='networkoption',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp at which the option instance of the network last updated'),
        ),
        migrations.AlterField(
            model_name='networkreview',
            name='by',
            field=models.ForeignKey(help_text='Reference to the user who is adding a review about the network', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='networkreview',
            name='comment',
            field=models.TextField(blank=True, help_text='Comment that the user made on the network', null=True),
        ),
        migrations.AlterField(
            model_name='networkreview',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp at which the review has been created'),
        ),
        migrations.AlterField(
            model_name='networkreview',
            name='id',
            field=models.CharField(blank=True, help_text='Primary key of the network reveiew', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='networkreview',
            name='is_active',
            field=models.BooleanField(default=True, help_text='If true, the review is active. If false the review has been deactivated'),
        ),
        migrations.AlterField(
            model_name='networkreview',
            name='is_spam',
            field=models.BooleanField(default=False, help_text='If true the review is marked as spam is not valid'),
        ),
        migrations.AlterField(
            model_name='networkreview',
            name='network',
            field=models.ForeignKey(help_text='reference to the network for whom review is going to be added', on_delete=django.db.models.deletion.CASCADE, to='network.network'),
        ),
        migrations.AlterField(
            model_name='networkreview',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5.0, help_text='Rating that user has given to the network', max_digits=2),
        ),
        migrations.AlterField(
            model_name='networkstaff',
            name='application_id',
            field=models.CharField(blank=True, help_text='Application ID of the Job Applicant', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='networkstaff',
            name='demoted_count',
            field=models.IntegerField(default=0, help_text='How much times the staff has been demoted by the network'),
        ),
        migrations.AlterField(
            model_name='networkstaff',
            name='id',
            field=models.CharField(blank=True, help_text='Primary Key of the Stafff', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='networkstaff',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Is the staff is currently working for the network'),
        ),
        migrations.AlterField(
            model_name='networkstaff',
            name='job',
            field=models.ForeignKey(help_text='Reference to the network job for which this staff has been hired', on_delete=django.db.models.deletion.CASCADE, to='network.networkjob'),
        ),
        migrations.AlterField(
            model_name='networkstaff',
            name='joined',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp at which the staff joined the network'),
        ),
        migrations.AlterField(
            model_name='networkstaff',
            name='profile',
            field=models.ForeignKey(help_text='Reference to the Job Profile of the Staff who has been selected for the job', on_delete=django.db.models.deletion.CASCADE, to='job_profiles.jobprofile'),
        ),
        migrations.AlterField(
            model_name='networkstaff',
            name='promoted_count',
            field=models.IntegerField(default=0, help_text='How much times the staff has been promoted by the network'),
        ),
        migrations.AlterField(
            model_name='networkstaff',
            name='updated',
            field=models.DateTimeField(auto_now=True, help_text='Timestamp at which the staff details last updated'),
        ),
        migrations.AlterField(
            model_name='networkstat',
            name='id',
            field=models.CharField(blank=True, help_text='Primary Key of the network Stat', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='networkstat',
            name='network',
            field=models.ForeignKey(help_text='Reference to the Network ', on_delete=django.db.models.deletion.CASCADE, to='network.network'),
        ),
        migrations.AlterField(
            model_name='networktype',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp at which network type is created'),
        ),
        migrations.AlterField(
            model_name='networktype',
            name='image',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text='Network Type display image', null=True),
        ),
        migrations.AlterField(
            model_name='networktype',
            name='name',
            field=models.CharField(blank=True, help_text='Name of the network type', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='networkvideo',
            name='id',
            field=models.CharField(blank=True, help_text='Primary key of the Network Video', max_length=10, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='networkvideo',
            name='label',
            field=models.CharField(blank=True, help_text='Label for the video specifying what the video depicts actually', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='networkvideo',
            name='network',
            field=models.ForeignKey(help_text='Reference to the network who is uploading the video', on_delete=django.db.models.deletion.CASCADE, to='network.network'),
        ),
        migrations.AlterField(
            model_name='networkvideo',
            name='video',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', help_text='Actual Video URL', null=True),
        ),
    ]

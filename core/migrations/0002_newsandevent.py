# Generated by Django 3.1 on 2020-10-12 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsAndEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, choices=[('news', 'News'), ('event', 'Event'), ('announcement', 'Announcement'), ('activity', 'Activity'), ('change_log', 'Change Logs'), ('feature_update', 'Feature Updates'), ('bug_fixes', 'Bug Fixes'), ('advertisement', 'Advertisement')], default='news', max_length=255, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('image_url', models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True)),
                ('upvotes', models.IntegerField(blank=True, default=0, null=True)),
                ('downvotes', models.IntegerField(blank=True, default=0, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

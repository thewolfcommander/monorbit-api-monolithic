# Generated by Django 3.1 on 2020-10-12 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greivances', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqcategory',
            name='image_url',
            field=models.URLField(blank=True, default='https://www.freeiconspng.com/thumbs/platform-icon/platform-icon-12.png', null=True),
        ),
    ]
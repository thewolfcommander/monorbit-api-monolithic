# Generated by Django 3.1 on 2020-10-12 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='thumbnail_image',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True),
        ),
        migrations.AlterField(
            model_name='productcustomcategory',
            name='image',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True),
        ),
        migrations.AlterField(
            model_name='productcustomsubcategory',
            name='image',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True),
        ),
        migrations.AlterField(
            model_name='productdefaultcategory',
            name='image',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True),
        ),
        migrations.AlterField(
            model_name='productdefaultsubcategory',
            name='image',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True),
        ),
        migrations.AlterField(
            model_name='productdocument',
            name='doc',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True),
        ),
        migrations.AlterField(
            model_name='productvideo',
            name='video',
            field=models.URLField(blank=True, default='https://monorbit-alpha.s3-us-west-2.amazonaws.com/Content/images/undraw_team_up_ip2x.svg', null=True),
        ),
    ]

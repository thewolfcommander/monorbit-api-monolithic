# Generated by Django 3.1 on 2020-10-12 12:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
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
                ('id', models.CharField(blank=True, max_length=20, primary_key=True, serialize=False, unique=True)),
                ('hash_token', models.CharField(blank=True, max_length=255, null=True)),
                ('full_name', models.CharField(blank=True, help_text='This will be the user full name', max_length=255, null=True, verbose_name='full_name')),
                ('email', models.EmailField(blank=True, help_text='This will be the user email', max_length=255, null=True, validators=[django.core.validators.EmailValidator, monorbit.utils.validators.custom_email_validator])),
                ('country_code', models.IntegerField(blank=True, default=91, null=True)),
                ('mobile_number', models.CharField(blank=True, error_messages={'invalid': 'Mobile number should be valid', 'required': 'Please provide your mobile number.', 'unique': 'An account with this mobile number exist.'}, help_text='This will be the user phone number', max_length=10, unique=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender'), ('Custom', 'Custom')], default='Male', max_length=30, null=True)),
                ('dob', models.CharField(blank=True, default='22-01-2000', max_length=100, null=True)),
                ('registration_reference', models.CharField(blank=True, default='None', max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('network_created', models.IntegerField(blank=True, default=0, null=True)),
                ('otp_sent', models.IntegerField(blank=True, default=0, null=True)),
                ('password_otp_sent', models.IntegerField(blank=True, default=0, null=True)),
                ('order_count', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('followed_networks', models.PositiveIntegerField(blank=True, default=0, null=True)),
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
        migrations.CreateModel(
            name='UserLocalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('communication_language_code', models.CharField(blank=True, choices=[('af', 'afrikaans'), ('sq', 'albanian'), ('am', 'amharic'), ('ar', 'arabic'), ('hy', 'armenian'), ('az', 'azerbaijani'), ('eu', 'basque'), ('be', 'belarusian'), ('bn', 'bengali'), ('bs', 'bosnian'), ('bg', 'bulgarian'), ('ca', 'catalan'), ('ceb', 'cebuano'), ('ny', 'chichewa'), ('zh-cn', 'chinese (simplified)'), ('zh-tw', 'chinese (traditional)'), ('co', 'corsican'), ('hr', 'croatian'), ('cs', 'czech'), ('da', 'danish'), ('nl', 'dutch'), ('en', 'english'), ('eo', 'esperanto'), ('et', 'estonian'), ('tl', 'filipino'), ('fi', 'finnish'), ('fr', 'french'), ('fy', 'frisian'), ('gl', 'galician'), ('ka', 'georgian'), ('de', 'german'), ('el', 'greek'), ('gu', 'gujarati'), ('ht', 'haitian creole'), ('ha', 'hausa'), ('haw', 'hawaiian'), ('iw', 'hebrew'), ('he', 'hebrew'), ('hi', 'hindi'), ('hmn', 'hmong'), ('hu', 'hungarian'), ('is', 'icelandic'), ('ig', 'igbo'), ('id', 'indonesian'), ('ga', 'irish'), ('it', 'italian'), ('ja', 'japanese'), ('jw', 'javanese'), ('kn', 'kannada'), ('kk', 'kazakh'), ('km', 'khmer'), ('ko', 'korean'), ('ku', 'kurdish (kurmanji)'), ('ky', 'kyrgyz'), ('lo', 'lao'), ('la', 'latin'), ('lv', 'latvian'), ('lt', 'lithuanian'), ('lb', 'luxembourgish'), ('mk', 'macedonian'), ('mg', 'malagasy'), ('ms', 'malay'), ('ml', 'malayalam'), ('mt', 'maltese'), ('mi', 'maori'), ('mr', 'marathi'), ('mn', 'mongolian'), ('my', 'myanmar (burmese)'), ('ne', 'nepali'), ('no', 'norwegian'), ('or', 'odia'), ('ps', 'pashto'), ('fa', 'persian'), ('pl', 'polish'), ('pt', 'portuguese'), ('pa', 'punjabi'), ('ro', 'romanian'), ('ru', 'russian'), ('sm', 'samoan'), ('gd', 'scots gaelic'), ('sr', 'serbian'), ('st', 'sesotho'), ('sn', 'shona'), ('sd', 'sindhi'), ('si', 'sinhala'), ('sk', 'slovak'), ('sl', 'slovenian'), ('so', 'somali'), ('es', 'spanish'), ('su', 'sundanese'), ('sw', 'swahili'), ('sv', 'swedish'), ('tg', 'tajik'), ('ta', 'tamil'), ('te', 'telugu'), ('th', 'thai'), ('tr', 'turkish'), ('uk', 'ukrainian'), ('ur', 'urdu'), ('ug', 'uyghur'), ('uz', 'uzbek'), ('vi', 'vietnamese'), ('cy', 'welsh'), ('xh', 'xhosa'), ('yi', 'yiddish'), ('yo', 'yoruba'), ('zu', 'zulu')], default='en', max_length=5, null=True)),
                ('interface_language_code', models.CharField(blank=True, choices=[('af', 'afrikaans'), ('sq', 'albanian'), ('am', 'amharic'), ('ar', 'arabic'), ('hy', 'armenian'), ('az', 'azerbaijani'), ('eu', 'basque'), ('be', 'belarusian'), ('bn', 'bengali'), ('bs', 'bosnian'), ('bg', 'bulgarian'), ('ca', 'catalan'), ('ceb', 'cebuano'), ('ny', 'chichewa'), ('zh-cn', 'chinese (simplified)'), ('zh-tw', 'chinese (traditional)'), ('co', 'corsican'), ('hr', 'croatian'), ('cs', 'czech'), ('da', 'danish'), ('nl', 'dutch'), ('en', 'english'), ('eo', 'esperanto'), ('et', 'estonian'), ('tl', 'filipino'), ('fi', 'finnish'), ('fr', 'french'), ('fy', 'frisian'), ('gl', 'galician'), ('ka', 'georgian'), ('de', 'german'), ('el', 'greek'), ('gu', 'gujarati'), ('ht', 'haitian creole'), ('ha', 'hausa'), ('haw', 'hawaiian'), ('iw', 'hebrew'), ('he', 'hebrew'), ('hi', 'hindi'), ('hmn', 'hmong'), ('hu', 'hungarian'), ('is', 'icelandic'), ('ig', 'igbo'), ('id', 'indonesian'), ('ga', 'irish'), ('it', 'italian'), ('ja', 'japanese'), ('jw', 'javanese'), ('kn', 'kannada'), ('kk', 'kazakh'), ('km', 'khmer'), ('ko', 'korean'), ('ku', 'kurdish (kurmanji)'), ('ky', 'kyrgyz'), ('lo', 'lao'), ('la', 'latin'), ('lv', 'latvian'), ('lt', 'lithuanian'), ('lb', 'luxembourgish'), ('mk', 'macedonian'), ('mg', 'malagasy'), ('ms', 'malay'), ('ml', 'malayalam'), ('mt', 'maltese'), ('mi', 'maori'), ('mr', 'marathi'), ('mn', 'mongolian'), ('my', 'myanmar (burmese)'), ('ne', 'nepali'), ('no', 'norwegian'), ('or', 'odia'), ('ps', 'pashto'), ('fa', 'persian'), ('pl', 'polish'), ('pt', 'portuguese'), ('pa', 'punjabi'), ('ro', 'romanian'), ('ru', 'russian'), ('sm', 'samoan'), ('gd', 'scots gaelic'), ('sr', 'serbian'), ('st', 'sesotho'), ('sn', 'shona'), ('sd', 'sindhi'), ('si', 'sinhala'), ('sk', 'slovak'), ('sl', 'slovenian'), ('so', 'somali'), ('es', 'spanish'), ('su', 'sundanese'), ('sw', 'swahili'), ('sv', 'swedish'), ('tg', 'tajik'), ('ta', 'tamil'), ('te', 'telugu'), ('th', 'thai'), ('tr', 'turkish'), ('uk', 'ukrainian'), ('ur', 'urdu'), ('ug', 'uyghur'), ('uz', 'uzbek'), ('vi', 'vietnamese'), ('cy', 'welsh'), ('xh', 'xhosa'), ('yi', 'yiddish'), ('yo', 'yoruba'), ('zu', 'zulu')], default='en', max_length=5, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordUpdateToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmailVerifyOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(blank=True, max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

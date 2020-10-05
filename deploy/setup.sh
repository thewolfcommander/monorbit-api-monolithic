#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/monorbit/monorbit-api-monolithic/'

PROJECT_BASE_PATH='/usr/local/apps/monorbit-api-monolithic'

echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev sqlite python3-pip supervisor nginx git

# Create project directory
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
pip3 install virtualenv
python3 -m virtualenv $PROJECT_BASE_PATH/env

# Install python packages
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip install uwsgi==2.0.18

# Setting up the envs variables
echo ```
SECRET_KEY=f$s@gkr!%!bxu^0sfj1w4a_x&a$dpn(0bk)&@grvlmn)mmh5&l
DEBUG=True
DB_NAME=monorbit
DB_USER=mono
DB_PASSWORD=iamtheman
DB_HOST=localhost
DB_POST=5432
LOG_FILE=mono_log.json
ENABLE_JSON_LOGGING=1
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=postmaster@mg.monorbit.com
SMTP_PASSWORD=146a1b4981013213f38f226798eb990c-4d640632-babc1148
MAILGUN_API_KEY=f381a922d34b77e8f7eb2b300486473a-1df6ec32-6ccd846f
MAILGUN_API_URL=https://api.mailgun.net/v3/mg.monorbit.com/messages
TWILIO_PHONE_NUMBER=+19016123660
TWILIO_ACCOUNT_SID=ACe9f5c189454598a110722ee2be46a341
TWILIO_AUTH_TOKEN=ef246cd29d4bc931ee7f645f4ae8512a
SENTRY_DSN=https://d99af8b497ae447184234d7e41bd4c8b@o438843.ingest.sentry.io/5404510
RAZORPAY_API_KEY=rzp_test_x1OuprBYA5F1x0
RAZORPAY_API_SECRET=JIV3BNXlHQh4pPEuIoztOPeA

HEROKU_DB_NAME=d74is14e7fcd2r
HEROKU_DB_USER=hvtkjsynlhhnom
HEROKU_DB_PASSWORD=647269ac29521116001d7c1f6d6ca9c00e7d42dfcbdf81a57b466f5f29fcf409
HEROKU_DB_HOST=ec2-54-166-107-5.compute-1.amazonaws.com
HEROKU_DB_POST=5432
``` > $PROJECT_BASE_PATH/.env

# Run migrations and collectstatic
cd $PROJECT_BASE_PATH
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput

# Configure supervisor
cp $PROJECT_BASE_PATH/deploy/supervisor_profiles_api.conf /etc/supervisor/conf.d/profiles_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart monorbit-api-monolithic

# Configure nginx
cp $PROJECT_BASE_PATH/deploy/nginx_profiles_api.conf /etc/nginx/sites-available/profiles_api.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/profiles_api.conf /etc/nginx/sites-enabled/profiles_api.conf
systemctl restart nginx.service

echo "DONE! :)"
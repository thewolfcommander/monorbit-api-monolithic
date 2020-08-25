git add . && git commit -m "Deployment started"
git push origin master
git push heroku master
heroku run python3 manage.py migrate --app monorbit-alpha
heroku config:set MAILGUN_API_URL=https://api.mailgun.net/v3/mg.monorbit.com/messages --app monorbit-alpha
heroku config:set MAILGUN_API_KEY=f381a922d34b77e8f7eb2b300486473a-1df6ec32-6ccd846f --app monorbit-alpha
heroku config:set SMTP_PASSWORD=146a1b4981013213f38f226798eb990c-4d640632-babc1148 --app monorbit-alpha
heroku config:set SMTP_USERNAME=postmaster@mg.monorbit.com --app monorbit-alpha
heroku config:set SMTP_PORT=587 --app monorbit-alpha
heroku config:set SMTP_SERVER=smtp.mailgun.org --app monorbit-alpha
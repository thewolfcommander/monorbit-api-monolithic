git add . && git commit -m "Deployment started"
git push origin master
git push heroku master
# heroku run python3 manage.py migrate --app monorbit-alpha

# heroku config:set TWILIO_PHONE_NUMBER=+19016123660 --app monorbit-alpha
# heroku config:set TWILIO_ACCOUNT_SID=ACe9f5c189454598a110722ee2be46a341 --app monorbit-alpha
# heroku config:set TWILIO_AUTH_TOKEN=ef246cd29d4bc931ee7f645f4ae8512a --app monorbit-alpha
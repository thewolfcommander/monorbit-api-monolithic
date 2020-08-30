git add . && git commit -m "Deployment started"
git push origin master
git push heroku master
heroku run python3 manage.py migrate --app monorbit-alpha

# heroku config:set  --app monorbit-alpha
git add . && git commit -m "Deployment started"
git push origin master
git push heroku master
heroku run python3 manage.py migrate --app monorbit-alpha

# heroku config:set SENTRY_DSN=https://d99af8b497ae447184234d7e41bd4c8b@o438843.ingest.sentry.io/5404510 --app monorbit-alpha
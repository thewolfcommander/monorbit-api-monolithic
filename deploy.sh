git add . && git commit -m "Adding Logging"
git push origin v1.1
git push heroku master
# heroku run python3 manage.py migrate --app monorbit-alpha

# heroku config:set  --app monorbit-alpha
# heroku config:set RAZORPAY_API_KEY=rzp_test_x1OuprBYA5F1x0 --app monorbit-alpha
# heroku config:set RAZORPAY_API_SECRET=JIV3BNXlHQh4pPEuIoztOPeA --app monorbit-alpha
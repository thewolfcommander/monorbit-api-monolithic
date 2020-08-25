import requests
from decouple import config

from data.email_templates import *

API_KEY = config('MAILGUN_API_KEY')
URL = config('MAILGUN_API_URL')
FROM_TEXT = "Monorbit Support"


def send_simple_message(subject, from_email, to_email, message):
	return requests.post(
		URL,
		auth=("api", API_KEY),
		data={"from": "{} <{}>".format(FROM_TEXT, from_email),
			"to": [to_email,],
			"subject": subject,
			"text": message
		})


def send_otp_email_verification(email, otp):
	return send_simple_message(
		subject=templates[0]["subject"],
		from_email=templates[0]["from_email"],
		to_email=email,
		message=otp_message(otp)
	)


def send_reset_password_otp(email, otp):
	return send_simple_message(
		subject=templates[1]["subject"],
		from_email=templates[1]["from_email"],
		to_email=email,
		message=forgot_otp_message(otp)
	)
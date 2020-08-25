import requests
from decouple import config

from data.email_templates import templates, otp_message

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

send_simple_message(
	subject=templates[0]["subject"],
	from_email=templates[0]["from_email"],
	to_email="manoj@monorbit.com",
	message=otp_message(5422)
)
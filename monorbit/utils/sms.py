from twilio.rest import Client
from decouple import config


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
phone_number = config('TWILIO_PHONE_NUMBER')
client = Client(account_sid, auth_token)


def send(body, to_phone):
    try:
        message = client.messages.create(
                     body=body,
                     from_=phone_number,
                     to=to_phone
                 )
        return message.sid
    except:
        return "Error occured in sending OTP."


def verify_mobile(mobile_number, otp):
    body = """
Your OTP for Monorbit is {} and valid for 10 minutes. Please Do not share this with anyone.
In case of any problem, mail us at admin@monorbit.com
    """.format(otp)
    return send(body, mobile_number)


def reset_password(mobile_number, otp):
    body = """
Your OTP to reset password on Monorbit is {} and valid for 10 minutes. Please Do not share this with anyone.
In case of any problem, mail us at admin@monorbit.com
    """.format(otp)
    return send(body, mobile_number)


def greeting(mobile_number):
    body = """
Thank you for joining Monorbit Platform. We are happy to see you onboard.
We promise to grow your business with least effort from you.
Create you network here: https://business.monorbit.com
    """
    return send(body, mobile_number)

# mobile_number = "+918958805692"
# greeting(mobile_number)
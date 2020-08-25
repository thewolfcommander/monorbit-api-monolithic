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
    Hi, please enter the below OTP to verify your mobile number for Monorbit.
    OTP - {}.
    Please do not share this with anyone
    """.format(otp)
    return send(body, mobile_number)


def reset_password(mobile_number, otp):
    body = """
    Hi, please enter the below OTP to reset your password for Monorbit.
    OTP - {}.
    Please do not share this with anyone
    """.format(otp)
    return send(body, mobile_number)


def greeting(mobile_number):
    body = """
    Thank you for joining Monorbit Platform. We are happy to see you onboard.
    We promise to grow your business with least effort from you.
    Explore more here: https://www.monorbit.com
    """
    return send(body, mobile_number)

# mobile_number = "+918958805692"
# greeting(mobile_number)
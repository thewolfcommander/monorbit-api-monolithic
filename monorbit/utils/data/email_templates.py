def otp_message(otp):
    return """
Hi,

Thanks for using Monorbit Platform! Please confirm your email address by entering the OTP given below on the Application. We'll communicate with you via email from time to time so it's important that we have an up-to-date email address on file.

OTP - {}
This OTP is valid for 10 minutes only.

If you did not sign up for a Monorbit Email verification request, please disregard this email.

Happy Business!
The Monions
                """.format(str(otp))


def forgot_otp_message(otp):
    return """
Hi,

Thanks for using Monorbit Platform! We know that it hurts when you lost the password of such an amazing platform. But don't worry we are always here for you. Please enter the OTP given below in order to reset your Monorbit Account Password.

OTP - {}
This OTP is valid for 10 minutes only.

If you haven't requested the OTP for resetting your password, please disregard this email.

Happy Business!
The Monions
                """.format(str(otp))            


templates = [
    {
        "subject": "Hi! Please verify your email on Monorbit Platform",
        "from_email": "no-reply@monorbit.com",
    },
    {
        "subject": "Hi! Please reset your password using this OTP on Monorbit Platform",
        "from_email": "no-reply@monorbit.com",
    },
]
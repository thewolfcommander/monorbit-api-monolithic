"""
This module contains custom validations for the fields
"""

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def custom_email_validator(email):
    """
    This function will check whether the email contains the popular domains or not
    """
    if "@gmail.com" in email or "@yahoo.com" in email or "@hotmail.com" in email:
        return email
    else:
        raise ValidationError("This type of email is not supported")


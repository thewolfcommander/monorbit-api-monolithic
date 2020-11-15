from datetime import datetime

import random
import string
from django.utils import timezone
from django.utils.text import slugify


rzp_webhook_secret = 'gzrqd38il5vhp058oz6pg0r7d80l8bak8tw6wivisu6g61gkdn0rox120201010185439'

def label_gen(prefix):
    date = timezone.now()
    return "{}{}{}{}{}{}{}".format(prefix, date.year, date.month, date.day, date.hour, date.minute, date.second)

def item_code_generator(network):
    date = timezone.now()
    return "{}{}{}{}".format(network, date. date.hour, date.minute, date.second)


def short_url_id_gen():
    string = "QERWTYUEPOAPIJBJHBXGVXC"
    num = random.randint(0, 18)
    date = timezone.now()
    return "{}{}{}{}".format(string[num], string[num+1], date.minute, date.second)


def random_number_generator(start, end):
    main_num = random.randint(start, end)
    return main_num


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# print(label_gen(random_string_generator(size=55)))

def unique_slug_generator(instance, new_slug=None):
    """
    This is for generating a unique slug for the model and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    print(slug)
    return slug


def username_generator(name):
    names = name.split(" ")
    first_letter = names[0][0]
    try:
        three_letters_surname = names[-1][:10]
    except:
        three_letters_surname = random_string_generator(size=5)
    number = '{:03d}'.format(random.randrange(1, 99999))
    username = (first_letter + three_letters_surname + number)
    return username

# username_generator("Monosrbit Business")



def valid_username(username):
    """
    To validate the Username and Clean it for authentication purpose
    """
    # from django.contrib import messages
    special = "`~!@#$%^&*()_-+=\{\}[];':\",<.>/? "

    for i in username:
        if i in special:
            messages.error(request, 'Username can only contain alphabets')
            return False

    return True
import random
import string
from django.utils import timezone
from django.utils.text import slugify


def label_gen(prefix):
    date = timezone.now()
    return "{}-{}{}{}{}{}{}".format(prefix, date.year, date.month, date.day, date.hour, date.minute, date.second)


def random_number_generator():
    main_num = random.randint(1066545465, 6454635465) + random.randint(3066445465, 9786287465)
    print(main_num)
    return main_num


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



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
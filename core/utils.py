from django.utils.crypto import get_random_string
from string import digits, ascii_lowercase


def create_pin(size=5, chars=digits):
    return get_random_string(size, chars)


def create_random_code(size=10, chars=digits+ascii_lowercase):
    return get_random_string(size, chars)


def generate_pin_code(instance, size=5):
    code = create_pin(size=size)

    user_class = instance.__class__
    user_obj = user_class.objects.filter(pin=code)
    if user_obj.exists():
        return generate_pin_code(size=size)

    return code


def generate_invitation_code(instance, size=7):
    code = create_random_code(size)

    invitation_class = instance.__class__
    invitation_objs = invitation_class.objects.filter(code=code)
    if invitation_objs.exists():
        return generate_invitation_code(size=size)
    
    return code


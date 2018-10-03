from django.utils.crypto import get_random_string
from string import digits


def create_pin(size=5, chars=digits):
    return get_random_string(size, chars)


def generate_pin_code(instance, size=5):
    code = create_pin(size=size)

    user_class = instance.__class__
    user_obj = user_class.objects.filter(pin=code)
    if user_obj.exists():
        return generate_pin_code(size=size)

    return code
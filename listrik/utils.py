from string import digits
from django.utils.crypto import get_random_string

def create_trx_code(size=10, chars=digits):
    return get_random_string(size, chars)

def generate_trx(instance, size=10, prefix='400'):
    code = prefix + create_trx_code(size=size)

    trx_class = instance.__class__
    trx_exist = trx_class.objects.filter(trx_code=code).exists()
    if trx_exist:
        return generate_trx(instance)
    
    return code
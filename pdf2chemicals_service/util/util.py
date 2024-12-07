import random
import string

def generate_random_alphanumeric_sequence(size: int):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(size))
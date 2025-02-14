import os
import random
import string

def generate_random_alphanumeric_sequence(size: int):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(size))

def file_exists(file_path: str) -> bool:
    if os.path.exists(file_path):
        return True
    
    return False

def remove_file(file_path: str):
    if file_exists(file_path):
        os.remove(file_path)
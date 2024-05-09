import base64
from django.contrib.auth.base_user import BaseUserManager


def generate_random_password():
    print("here")
    return BaseUserManager().make_random_password()

def encrypt(pas):
    encoded_string = base64.b64encode(pas.encode('utf-8'))
    return encoded_string.decode('utf-8')

def decrypt(pas):
    decoded_string = base64.b64decode(pas.encode('utf-8'))
    return decoded_string.decode('utf-8')

import os
import jwt
from services.exceptions import InvalidResponse
from datetime import datetime, timedelta

def generate_jwt(payload, lifetime=None):
    # Lifetime of the token can be changed accordingly
    if lifetime:
        payload['exp'] = (datetime.now() + timedelta(minutes=lifetime)).timestamp()
        try:
            return jwt.encode(payload, os.getenv('SECRET_KEY', None), algorithm='HS256')
        except Exception as e:
            raise InvalidResponse("Error occured while generating the token!", 400)
    else:
        return None

def decode_jwt(token):
    # Retrieves the token and checks the validity
    return jwt.decode(token, os.getenv('SECRET_KEY', None), algorithms=["HS256"])
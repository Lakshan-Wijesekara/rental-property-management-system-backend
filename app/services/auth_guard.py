from flask import make_response, request
from services.http_responses import HttpResponse
from services.jwt_handler import decode_jwt
from services.exceptions import InvalidResponse
from functools import wraps
from datetime import datetime, timedelta

def check_jwt():
    #Get the token from request headers
    token = request.headers.get('Authorization')

    if not token:
        raise InvalidResponse("Access token is missing", 403)
    
    if not token.startswith("Bearer "):
        raise InvalidResponse("Invalid token format", 403)
    #Token is coming as (Bearer 1234&8484##) format, to get the jwt Bearer and the space is ommitted here
    jwt = token.split('Bearer ')[1] 
    try:
        return decode_jwt(jwt)
    except Exception:
        raise Exception("Invalid token!")
    
def auth_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS':
            return make_response("PreFlight Passed",204)
        try:
            user_data = check_jwt()
        except Exception as e:
            return HttpResponse().errorResponse("Authorization failed!", 401)
        return route_function(*args, **kwargs)
    #This returns the protected version of the route, wrapped version of the route
    return decorated_function

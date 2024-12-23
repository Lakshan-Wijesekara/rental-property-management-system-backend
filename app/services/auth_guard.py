from datetime import datetime, timedelta
from flask import make_response, request
from services.http_responses import HttpResponse
from services.jwt_handler import decode_jwt
from services.exceptions import InvalidResponse
from services.jwt_handler import generate_jwt
from functools import wraps

def check_jwt():
    #Get the token from request headers
    token = request.headers.get('Authorization')

    if not token:
        raise InvalidResponse("Access token is missing", 403)
    
    if not token.startswith("Bearer "):
        raise InvalidResponse("Invalid token format", 403)
    #Token comes as (Bearer 1234&8484##) format, to get the jwt Bearer and the space is ommitted here
    jwt = token.split('Bearer ')[1] 
    try:
        return decode_jwt(jwt)
    except Exception:
        raise Exception("Invalid token!")
    
def auth_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS':
            return make_response("PreFlight Passed", 204)
        try:
            user_data = check_jwt()
            if user_data:
                new_token = generate_jwt(payload=user_data, lifetime=5)
                response = make_response(route_function(*args, **kwargs))
                response.headers['NewAuthToken'] = f'Bearer {new_token}'
                return response

        except Exception as e:
            return HttpResponse().errorResponse(f'Authorization failed!: {e}', 401)
        
        return route_function(*args, **kwargs)
    #This returns the protected version of the route, wrapped version of the route
    return decorated_function

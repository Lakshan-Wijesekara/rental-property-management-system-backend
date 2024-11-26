from pymongo import errors
from services.http_responses import HttpResponse

http_response = HttpResponse()

class CustomExceptions:
    def app_exceptions(self, error):
        if isinstance(error, TypeError):
            return http_response.errorResponse(str(error),400)
        
        elif isinstance(error, ValueError):
            return http_response.errorResponse(str(error),400)
        
        elif isinstance(error, errors.DuplicateKeyError):
            return http_response.errorResponse(str(error),409)
        
        elif isinstance(error, errors.NetworkTimeout):
            return http_response.errorResponse(str(error),504)
        
        elif isinstance(error, errors.ConnectionFailure):
            return http_response.errorResponse(str(error),500)
        
        else:
            return http_response.errorResponse("An unexpected error occurred!",500)
        


        

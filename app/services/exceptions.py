from pymongo import errors
from services.http_responses import HttpResponse

http_response = HttpResponse()

class CustomExceptions:
    def app_exceptions(self, error):
        if isinstance(error, TypeError):
            return http_response.errorResponse("Invalid document type!",400)
        
        elif isinstance(error, ValueError):
            return http_response.errorResponse("Value error occurred, please check the data type!",400)
        
        elif isinstance(error, errors.DuplicateKeyError):
            return http_response.errorResponse("Duplicate key error, the record already exists!",409)
        
        elif isinstance(error, errors.NetworkTimeout):
            return http_response.errorResponse("Network timeout occurred, please check your network connection!",504)
        
        elif isinstance(error, errors.ConnectionFailure):
            return http_response.errorResponse("Connection refused, please check your network connection!",500)
        
        else:
            return http_response.errorResponse("An unexpected error occurred!",500)
        


        

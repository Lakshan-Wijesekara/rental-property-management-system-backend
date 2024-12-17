from pymongo import errors
from services.http_responses import HttpResponse

http_response = HttpResponse()

class CustomExceptions:

    exception_list = {
        TypeError: ("Invalid document type!", 400),
        ValueError: ("Value error occurred, please check the data type!", 400),
        errors.DuplicateKeyError:("Duplicate key error, the record already exists!", 409),
        errors.NetworkTimeout: ("Network timeout occurred, please check your network connection!", 504),
        errors.ConnectionFailure: ("Connection refused, please check your network connection!", 500),
    }

    def app_exceptions(self, error):
        #Get the type of error
        error_class_name = type(error) 
        try:
            #If the incoming error comes as a custom defined error
            if error_class_name==InvalidResponse:
                return http_response.errorResponse(error.message, error.status_code)
            get_error = self.exception_list.get(error_class_name, ("An unexpected error occurred!", 400))

            return http_response.errorResponse(*get_error)
        except Exception as error:
            return http_response.errorResponse(str(error), 400)


class InvalidResponse(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        self.type = "Custom_Error"      
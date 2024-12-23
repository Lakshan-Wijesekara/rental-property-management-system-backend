
class HttpResponse():

    def successResponse(self, data, status_code=200):
        success_response = {
            "status": "success",
            "message": "Operation was successful!",
            "data":data
        }
        return success_response, status_code
      
    def errorResponse(self, error, status_code):
        error_response = {
            "status": "Failed",
            "message": "An error occured while operation!",
            "error detail":error
        }
        return error_response, status_code
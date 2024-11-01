from flask import make_response, jsonify

class HttpResponse:
    def successResponse(self, data):
        success_response = {
            "status": "success (200)",
            "message": "Operation was successful!",
            "data":data
        }
        return success_response
    
    def errorResponse(self, error):
        error_response = {
            "status": "Failed",
            "message": "An error occured while operation!",
            "error detail":error
        }
        return error_response

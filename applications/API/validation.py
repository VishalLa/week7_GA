import json
from flask import make_response
from werkzeug.exceptions import HTTPException

# For 404
class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response(status_code=status_code)


# For 409
class DuplicateError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response(status_code=status_code)


# Student API Error 
class StudentValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        data = {
              'error_code': error_code,
              'error_message': error_message
         }
        self.response = make_response(json.dump(data), status_code)


# Course API Error
class CourseValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        data = {
              'error_code': error_code,
              'error_message': error_message
          }
        self.response = make_response(json.dump(data), status_code)


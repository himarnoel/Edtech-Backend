# utils.py

from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Check if the response contains non-field errors
        if 'non_field_errors' in response.data:
            # Extract and format non-field errors
            errors = response.data['non_field_errors']
            response.data = {'error': errors}
        else:
            # Flatten the error structure
            error_message = ''
            if isinstance(response.data, dict):
                error_message = list(response.data.values())[0][0] if response.data else 'An error occurred'
            else:
                error_message = response.data[0] if response.data else 'An error occurred'
            response.data = {'error': error_message}

    return response

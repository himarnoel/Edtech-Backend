from rest_api_payload import success_response, error_response
def error_message(message):
    payload=error_response(
            status="Failed",
            message=message
    )
    return payload

def success_message(data, message):
    payload= success_response(
                status="Success",
                message=message, 
                data=data    
            )
    return payload
import logging
from rest_framework.views import exception_handler
import logging

logger = logging.getLogger('exception.handler')
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    # if response is not None:
    #     logger.info(f"aaaaaa:::{response.data[0]['status_code']}")
    #     response.data['status_code'] = response.status_code

    return response
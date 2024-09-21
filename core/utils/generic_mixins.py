
from rest_framework.response import Response
from rest_framework import status as status_code

from core.utils.constants import ERROR_MSG, SUCCESS_MSG

class ResponseMixin:
    """
    Response class with different response methods
    """
    def error_response(self, msg=ERROR_MSG, **kwargs):
        """for error response"""
        return Response(
            {"message": msg, **kwargs},
            status=status_code.HTTP_400_BAD_REQUEST,
        )

    def success_response(self, msg=SUCCESS_MSG, **kwargs):
        """for success response"""
        return Response(
            {"message": msg, **kwargs},
            status=status_code.HTTP_200_OK,
        )

import logging
from rest_framework import views, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.authentication.v1.serializers import AccountsLoginSerializer, AccountsUserRegistrationSerializer
from core.settings import logger
from core.utils.generic_mixins import ResponseMixin


class AccountsUserRegistrationAPIView(views.APIView, ResponseMixin):
    serializer_class = AccountsUserRegistrationSerializer
    api_logger = logging.LoggerAdapter(
        logger, {"app_name": "AccountsUserRegistrationAPIView"}
    )
    """
    API for registering users
    """
    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(
                data=data,
                context={
                    "logger" : self.api_logger,
                    "request" : request
                    })
            if serializer.is_valid():
                serializer.save()
                return self.success_response(msg="User created successfully")
            return self.error_response(msg = serializer.errors)
        except Exception as e:
            self.api_logger.info(f"AccountsUserRegistrationAPIView POST, {str(e)}")
            return self.error_response(data=str(e))

class AccountsLoginAPIView(TokenObtainPairView):
    serializer_class = AccountsLoginSerializer

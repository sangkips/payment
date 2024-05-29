import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.serializers import RegisterSerializer


# Create your views here.


class GenericViewSet(ViewSet):
    http_method_names = ['get', 'put', 'post', 'patch', ]
    permission_classes = [AllowAny, ]

class AuthenticationView(GenericViewSet):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={200: openapi.Response('Success', RegisterSerializer),
                   400: 'Bad Request'},
    )
    
    def register(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            # access_token = AuthenticationHandler.create_access_token(request, user=user)
            
            return Response(
                {
                    "success": True,
                    'data': {
                        "id": user.id,
                        "uuid": user.uuid,
                        "firstName": user.first_name,
                        "lastUpdatedPassword": user.last_updated_password,
                        "email": user.email,
                        "emailVerified": user.email_verified,
                    }
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
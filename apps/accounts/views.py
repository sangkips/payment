import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.serializers import LoginSerializer, RegisterSerializer
from apps.accounts.tasks import LoginHandler, UserHandler


# Create your views here.


class GenericViewSet(ViewSet):
    http_method_names = ['get', 'put', 'post', 'patch', ]
    permission_classes = [AllowAny, ]

class AuthenticationView(GenericViewSet):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={200: openapi.Response('Success', LoginSerializer),
                   400: 'Bad Request'},
        tags=['Account']
    )
    
    def register(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            return Response(
                {
                    "success": True,
                    'data': {
                        "id": user.id,
                        "uuid": user.uuid,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "email": user.email,
            
                    }
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response(
                {"status": status.HTTP_400_BAD_REQUEST, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
    
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: openapi.Response('Success', LoginSerializer),
                   400: 'Bad Request'},
        tags=['Account']
    )
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        
        # Validate the serializer
        if not serializer.is_valid():
            return Response(
                {
                    "status": serializer.errors.get("status", ["Invalid data"])[0],
                    "message": serializer.errors.get("message", ["Invalid data"])[0]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data["email"].lower()
        
        # Retrieve the user
        user = UserHandler.get_user(email=email)
        if not user:
            return Response(
                {
                    "success": False,
                    "message": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        password = serializer.validated_data['password']
        
        # Authenticate the user
        try:
            user_data = LoginHandler(user, request).login_authenticator(password)
        except Exception as e:
            logging.info(e)
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "success": True,
                "data": user_data
            },
            status=status.HTTP_200_OK
        )

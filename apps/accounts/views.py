from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

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
    
    def register():
        pass
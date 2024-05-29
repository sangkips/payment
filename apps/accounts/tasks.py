import logging
from oauthlib.oauth2.rfc6749.tokens import random_token_generator
from django.conf import settings
from apps.accounts.crud import AccessTokenCRUD
class AuthenticationHandler:

    @staticmethod
    def create_access_token(request, user, scope=settings.OAUTH2_PROVIDER['SCOPES']):
        """
        Create access token for user with scope(custom or default)
        """
        try:
            token = random_token_generator(request)
            return AccessTokenCRUD(
                user=user,
                token=token,
                scope=scope
            ).create()
        except Exception as error:
            logging.error(error)
            return False

import uuid
from abc import ABCMeta, abstractmethod
import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
import logging
from django.db.models import Q
from oauth2_provider.models import AccessToken, Application

logging = logging.getLogger('accounts_crud')

User = get_user_model()


class IModels(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def create():
        """This function will act as an interface """

class AccessTokenCRUD(IModels):
    def __init__(self, token, user=None, scope=None):
        self.token = token
        self.user = user
        self.application = Application.objects.get(name="payments")
        self.expire_seconds = settings.OAUTH2_PROVIDER[
            'ACCESS_TOKEN_EXPIRE_SECONDS']
        self.expires = datetime.datetime.now() + datetime.timedelta(
            seconds=self.expire_seconds
        )
        self.scopes = scope or settings.OAUTH2_PROVIDER['SCOPES']

    def create(self):
        try:
            access_token = AccessToken.objects.create(
                user=self.user,
                application=self.application,
                token=self.token,
                expires=self.expires,
                scope=self.scopes
            )
            return access_token
        except Exception as error:
            logging.info(error)
            return False

    def update(self, **kwargs):
        try:
            access_token = AccessToken.objects.filter(
                token=self.token
            ).filter(
                **kwargs
            )
            return access_token
        except Exception as error:
            logging.info(error)
            return False

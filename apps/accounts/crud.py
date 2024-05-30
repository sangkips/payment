import uuid
from abc import ABCMeta, abstractmethod
import datetime
from django.utils import timezone
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

class UserHandlerOBJ(IModels):
    def __init__(self, first_name, middle_name, last_name,
                 email, user_uuid=None, pk=None, email_verified=False,
                 password=None):
        self.pk = pk
        self.user_uuid = user_uuid
        self.first_name = first_name
        self.email = email
        self.last_name = last_name
        self.middle_name = middle_name
        self.email_verified = email_verified
        self.password = password
        
    # This method will be used to create user instances
    def create(self):
       
        try:
            user = User.objects.create(
                first_name=self.first_name,
                last_name=self.last_name,
                middle_name=self.middle_name,
                email=self.email,
                email_verified=self.email_verified,
                account_type=self.account_type,
                password=self.password,
                uuid=uuid.uuid4()
            )
            return user
        except Exception as error:
            logging.info(error)
            return False

    # This function can be used to get user using uuid, email, pk
    @staticmethod
    def get_user(email=None, pk=None, user_uuid=None):
        try:
            if email:
                user = User.objects.get(email=email)
            elif pk:
                user = User.objects.get(pk=pk)
            else:
                user = User.objects.get(uuid=user_uuid)
            return user
        except Exception as error:
            logging.info(f"Expected and handled error: {error}")
            raise error

    #  This function will be used to update user's bio data
    def update_user_bio_data(self):
 
        try:
            updated = User.objects.filter(
                Q(email=self.email),
                Q(uuid=self.user_uuid)
            ).update(
                first_name=self.first_name,
                last_name=self.last_name,
                middle_name=self.middle_name,
            )
            return updated
        except Exception as error:
            logging.info(error)
            return False

    # This function will be used to update user's password
    @staticmethod
    def update_password(user, encrypted_password):
  
        try:
            user.password = encrypted_password
            user.save()
            return user
        except Exception as error:
            logging.info(error)
            return False

    #  This function will be used to update user's last password update
    @staticmethod
    def update_last_login(user):
     
        try:
            user.last_login = timezone.now()
            user.save()
            return user
        except Exception as error:
            logging.info(error)
            return False

    # This function will be used to update user
    @staticmethod
    def update_user(user_uuid, **kwargs):
        try:
            User.objects.filter(
                uuid=user_uuid
            ).update(
                **kwargs
            )
            return User.objects.get(uuid=user_uuid)
        except Exception as error:
            logging.info(error)
            return False
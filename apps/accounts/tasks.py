import logging
import binascii
from oauthlib.oauth2.rfc6749.tokens import random_token_generator
from django.conf import settings
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF1
from Crypto.Random import get_random_bytes

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


class PasswordEncryption:
    def __init__(self, password):
        self.password = password

    # hash for new user when signin up
    def encrypt_password(self):
        salt = get_random_bytes(8)
        keys = PBKDF1(
            self.password, salt,
            32, count=1000,
            hashAlgo=SHA256
        )
        # append the salt to the hashed password
        # for comparison
        hashed_pass = keys + salt
        # hexlify the password to store in db
        decode_hash = binascii.hexlify(hashed_pass).decode()
        return decode_hash

    # Compare Passwords
    @staticmethod
    def compare_passwords(password, stored_password):
        try:
            stored_password = stored_password.encode()
            decode_password = binascii.unhexlify(stored_password)
            salt = decode_password[32:]
            # generate the keys using salt and sha256
            keys = PBKDF1(password, salt, 32, count=1000, hashAlgo=SHA256)
            # append the salt to the hashed password
            # for comparison
            hashed_pass = keys + salt
            # convert to hexadecimal and hash the password
            decode_hash = binascii.hexlify(hashed_pass).decode()
            if decode_hash == stored_password.decode():
                return True
            else:
                return False
        except Exception as error:
            logging.info(error)
            return False
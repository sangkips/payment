import logging
import uuid
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from decouple import config
import re
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException

from apps.accounts.tasks import PasswordEncryption, UserHandler


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "first_name", 'last_name', "email",
            "password",
        )
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        try:
            user_profile = super().create(validated_data)
            password_hash = PasswordEncryption(
                validated_data['password']).encrypt_password()
            user_profile.password = password_hash
            user_profile.uuid = uuid.uuid4()
            user_profile.email = validated_data["email"].lower()
            user_profile.save()
            return user_profile
        except Exception as error:
            logging.info(error)
            raise ValidationError({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": f"{error}"

            })

    @staticmethod
    def validated_password(password):
        passwd = password
        reg = config("PASSWORD_REG_EXP")

        # compiling regex
        pat = re.compile(reg)

        # searching regex
        mat = re.search(pat, passwd)

        # validating conditions
        if mat:
            return
        else:
            raise ValidationError({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Password doesnt meet requirements"
            })

    def validate(self, data):
        if not data["first_name"].isalpha():
            raise ValidationError({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "First Name must only be letters"

            })

        if len(data["first_name"]) <= 1:
            raise ValidationError({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "First Name Must be longer than one letter"
            })

        self.validated_password(data['password'])
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
    # Convert email to lowercase for consistency
        email = email.lower()
    
    # Retrieve the user associated with the given email
        user = UserHandler.get_user(email=email)
        
        # Check if the user exists
        if not user:
            raise APIException({
                "success": False,
                "message": "Incorrect email or password.",
            })
        
        # Check if the user's email is verified
        if not user.email_verified:
            raise APIException({
                "success": False,
                "message": "Please verify your email to continue",
            })
    
        return email
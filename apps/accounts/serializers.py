from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from decouple import config
import re
from django.core.exceptions import ValidationError


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

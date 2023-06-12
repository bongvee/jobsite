from rest_framework import serializers
from django.contrib.auth.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

        # VALIDATION
        extra_kwargs = {
            'first_name': { 'required': True, 'allow_blank': False },
            'last_name': { 'required': True, 'allow_blank': False },
            'email': { 'required': True, 'allow_blank': False },
            'password': { 'required': True, 'allow_blank': False, 'min_length': 5 },
        }

# SIGN IN
class UserSerializer(serializers.ModelSerializer):
    ident_card = serializers.CharField(source='userprofile.ident_card')     # for file upload
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'ident_card')


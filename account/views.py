from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes  # auth
from rest_framework.permissions import IsAuthenticated              # auth
from rest_framework.response import Response

from django.contrib.auth.hashers import make_password               # password hash
from django.contrib.auth.models import User
from .serializers import SignUpSerializer, UserSerializer

@api_view(['POST'])
def signup_user(request):     # register
    data = request.data

    user = SignUpSerializer(data=data)

    # check if user entries are valid
    if user.is_valid():
        # if yes, check if user already exists
        if not User.objects.filter(email=data['email']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                username = data['username'],
                email = data['email'],
                password = make_password(data['password']),     # hash and save password
            )

            return Response({
                'message': 'SUCCESS! User has been signed up.'},
                status = status.HTTP_200_OK
            )
        
        else:
            # if user already exists
            return Response({
                'error': 'SORRY. User EMAIL already exist.'},
                status = status.HTTP_400_BAD_REQUEST
            )

    else:
        # if user entries are not valid, show errors
        return Response(user.errors)


# get current user
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # check if user is authenticated
def currentUser(request):

    user = UserSerializer(request.user)
    return Response(user.data)
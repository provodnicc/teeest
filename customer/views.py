from urllib import response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response


from .models import User
from .serialize import UserSerializer
from .methods import getPayload, getToken

import jwt, datetime
# Create your views here.   
from django.shortcuts import render

def registration(request):
    try:
        return render(request, 'SignUp.html')
    except:
        return render(request, 'Error.html')
def auth(request):
    try:
        return render(request, 'Auth.html')
    except:
        return render(request, 'Error.html')

class SignUpView(APIView):
    def post(self, request):
        serializer =  UserSerializer (data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class SignInView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        token = getToken(user)

        response = Response()
        response.set_cookie(key='token', value=token, httponly=True)
        response.data = {
            "token" : token
        }
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed('User not found!')

        try:
            payload = getPayload(token)
        except:
            raise AuthenticationFailed('User not found!')

        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)
        return Response(serializer.data)

class checkUserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed('Log in please')
        try:
            payload = getPayload(token)
        except:
            raise AuthenticationFailed('Auth error')
        user = User.objects.filter(id=payload['id']).first()
        token = getToken(user)
        response = Response(data="cool")

        response.set_cookie(key='token', value=token, httponly=True)
        return response


class LogOutView(APIView):
    def get(self, request):
        response = Response(status=200)
        response.delete_cookie('token')
        response.data = {
            'message' : 'success'
        }

        return response
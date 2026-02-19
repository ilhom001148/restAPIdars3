from django.shortcuts import render
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import SignUpSerizlizer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class SignUpView(APIView):
    def post(self,request):
        serializer=SignUpSerizlizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        response={
            'status':status.HTTP_201_CREATED,
            'message':user.username
        }
        return Response(response)

class LoginView(APIView):
    def post(self,request):
        username=self.request.data.get('username')
        password=self.request.data.get('password')

        user=authenticate(username=username,password=password)

        if not user:
            raise ValidationError({'message':'Username yoki parol notogri'})

        token,_=Token.objects.get_or_create(user=user)

        response={
            'status':status.HTTP_201_CREATED,
            'message':'Siz royxatdan otdingiz',
            'token':str(token.key)
            }
        return Response(response)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        response={
            'status':status.HTTP_200_OK,
            'message':'muvaffaqiyatli logout qilindi'
        }
        return Response(response)












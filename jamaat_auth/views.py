from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from . import models

import jwt, os
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response

from .serializer import CustomJamaatUserSerializer

from django.views import View



"""
API for auth
------------------
Include:
- register endpoint
- login endpoint
"""
class CustomJamaatUserAPIVIew(APIView):

    def __call__(self, request, *args, **kwargs):
        # Override __call__ to route the request to the appropriate method
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        response_data = {}

        try:
            data = request.data.copy()
            data['its'] = int(data['its'])

            serializer = CustomJamaatUserSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            # Create the user
            user = serializer.save()

            response_data = serializer.data

            jwt_token = jwt.encode(response_data, os.environ.get('DEH_JWT_TOKEN_SECRET'), algorithm='HS256')
            token_model = models.JamaatJWTTokenStore.objects.create(user_id=user, token_string=jwt_token)

            response_data['token'] = jwt_token

            response_data['status'] = status.HTTP_200_OK
        
        except Exception as e:
            response_data['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_data['error'] = 'Some error has occured. '

        return Response(response_data, status=response_data['status'])





class CustomJamaatUserLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        
        response_data = {}
        try:
            data = request.data.copy()
            mgmt_user_instance = authenticate(request, its=data.get('its'), password=data.get('password'))

            if mgmt_user_instance:

                data.pop('password')
                response_data = data
                response_data['name'] = mgmt_user_instance.full_name
                token = models.JamaatJWTTokenStore.objects.get(user_id = mgmt_user_instance).token_string
                response_data['status'] = status.HTTP_200_OK
                response_data['token'] = token
            else:
                response_data['status'] = status.HTTP_404_NOT_FOUND
                response_data['error'] = 'User not found. Please check your credentials.'
        except Exception as e:
            print(e)
            response_data['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_data['error'] = 'Some server error occured. Please try again sometime'
        
        return Response(response_data)

    











"""
Template view for Jamaat admin auth
--------------------------------------
Includes:
- HTML for jamaat login
"""
class ATJamaatAdminLogin(View):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

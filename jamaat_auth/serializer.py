from rest_framework import serializers
from . import models

from django.contrib.auth.hashers import make_password

"""
DEH Management users
--------------------
Include:
- management user serializer
"""

class CustomJamaatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomJamaatUser
        fields = ['its', 'password','jamaat']  # Include other fields as needed
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super(CustomJamaatUserSerializer, self).create(validated_data)
        return user



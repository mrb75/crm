from rest_framework import serializers
from .models import *


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['__all__']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        images = UserImageSerializer(many=True)
        exclude = ['date_joined', 'last_login',
                   'birth_date', 'images']
        extra_kwargs = {'password': {'write_only': True}}


class EditProfile(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    mobile = serializers.CharField()
    national_code = serializers.CharField()
    Gender = serializers.ChoiceField(choices=['Male', 'Female', 'Nothing'])

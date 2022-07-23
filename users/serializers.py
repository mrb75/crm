from rest_framework import serializers
from .models import *
import random
from django.contrib.auth.models import Group


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        images = UserImageSerializer(many=True)
        exclude = ['date_joined', 'last_login',
                   'birth_date', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserFormSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, default=None)
    last_name = serializers.CharField(max_length=100, default=None)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField(default=None)
    mobile = serializers.CharField(default=None)
    national_code = serializers.CharField(default=None)
    Gender = serializers.ChoiceField(
        choices=['Male', 'Female', 'Nothing'], default='Nothing')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'])
        for idx in validated_data.keys():
            if idx in ['email', 'first_name', 'last_name', 'gender', 'mobile', 'national_code']:
                setattr(user, idx, validated_data[idx])
        user.admin = validated_data['admin']
        user.set_password(''.join(random.sample(
            list('abcdefghigklmnopqrstuvwxyz'), 10)))
        if user.admin.is_superuser:
            user.groups.add(Group.objects.get(name='admin_user'))
        else:
            user.groups.add(Group.objects.get(name='end_user'))

        user.save()
        return user

    def update(self, instance, validated_data):
        user = instance
        for idx in validated_data.keys():
            if idx in ['email', 'first_name', 'last_name', 'gender', 'mobile', 'national_code']:
                setattr(user, idx, validated_data[idx])
        user.save()
        return user


class TicketSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'


class TicketFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def create(self, validated_data):
        ticket = Ticket.objects.create(user=validated_data['user'])
        for idx in validated_data.keys():
            setattr(ticket, idx, validated_data[idx])

        ticket.save()
        return ticket

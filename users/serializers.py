from rest_framework import serializers
from .models import *
import random
from django.contrib.auth.models import Group, Permission
from django.db.models import Q


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

    def create(self, validated_data, group=None):
        user = User(**validated_data)
        # user.username = validated_data['username']
        # for idx in validated_data.keys():
        #     if idx in ['email', 'first_name', 'last_name', 'gender', 'mobile', 'national_code']:
        #         setattr(user, idx, validated_data[idx])
        user.admin = validated_data['admin']
        user.set_password(''.join(random.sample(
            list('abcdefghigklmnopqrstuvwxyz'), 10)))
        user.save()
        if user.admin.is_superuser:
            user.groups.add(Group.objects.get(name='admin_user'))
        else:
            if group:
                user.groups.add(Group.objects.get(name=group))
            else:
                user.groups.add(Group.objects.get(name='end_user'))

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
        # ticket = Ticket.objects.create(user=validated_data['user'])
        # for idx in validated_data.keys():
        #     setattr(ticket, idx, validated_data[idx])
        ticket = Ticket(**validated_data)

        ticket.save()
        return ticket


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PermissionSetSerializer(serializers.Serializer):
    permission_id = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=1000)
    )

    def validate_permission_id(self, value):
        access_perms = Permission.objects.filter(Q(codename__contains='category')
                                                 | Q(codename__contains='product')
                                                 | Q(codename__contains='bill')
                                                 | Q(codename__contains='user')
                                                 | Q(codename__contains='turn')).values('id')
        access_ids = set(map(lambda x: x['id'], access_perms))
        if len(set(value)-access_ids):
            raise serializers.ValidationError(
                'you dont have access to some of permissions')
        return value


class TurnSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    coworker = UserSerializer(read_only=True)

    class Meta:
        model = Turn
        fields = '__all__'


class TurnFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = '__all__'

    def validate_user(self, value):
        if (value.admin == self.context['request'].user) or (value.admin == self.context['request'].user.admin):
            return value
        else:
            raise serializers.ValidationError('user is not belongs to you')

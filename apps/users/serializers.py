from django.db import transaction
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from apps.users.check_auth import get_refresh_token, blacklist
from apps.users import models as users_models
from apps.users.choices import UserRoleChoice


class CustomUserSerializer(serializers.ModelSerializer):
    raw_password = serializers.SerializerMethodField()

    class Meta:
        model = users_models.CustomUser
        fields = [
            'id',
            'phone',
            'full_name',
            'role',
            'raw_password',
            'created_at',
        ]

    @extend_schema_field(str)
    def get_raw_password(self, obj):
        return obj.raw_password.raw_password if hasattr(obj, 'raw_password') else None


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=9, min_length=9, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, attrs):
        return get_refresh_token(attrs.get('phone'), attrs.get('password'))


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=300)
    refresh = serializers.CharField(max_length=300)
    user = CustomUserSerializer()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=300)

    def validate(self, attrs):
        return blacklist(attrs.get('refresh'))


class CustomUserCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=9, min_length=9, required=True)
    full_name = serializers.CharField(max_length=50, required=True)
    role = serializers.ChoiceField(choices=UserRoleChoice.choices, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = users_models.CustomUser
        fields = ['phone', 'full_name', 'role', 'password']

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = users_models.CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        users_models.CustomUserPasswordLog.objects.update_or_create(user=user, defaults={"raw_password": password})
        return user


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=9, min_length=9, required=False)
    full_name = serializers.CharField(max_length=50, required=False)
    role = serializers.ChoiceField(choices=UserRoleChoice.choices, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = users_models.CustomUser
        fields = ['phone', 'full_name', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        if password:
            instance.set_password(password)
            users_models.CustomUserPasswordLog.objects.update_or_create(user=instance,
                                                                        defaults={"raw_password": password})
        instance.save()
        return instance
from django.db import transaction
from rest_framework import serializers
from apps.fields.models import Field
from apps.users.models import CustomUser
from utils.base64 import check_is_base64, base64_to_file, delete_old_file
from utils.exceptions import raise_error, ErrorCodes


class FieldCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    owner = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), required=False
    )

    class Meta:
        model = Field
        fields = [
            'owner',
            'name',
            'address',
            'contact',
            'price_per_hour',
            'latitude',
            'longitude',
            'images',
        ]

    def validate(self, data):
        images = data.get('images', getattr(self.instance, 'images', None))

        if images and not all(check_is_base64(img) for img in images):
            raise_error(
                ErrorCodes.INVALID_FILE_FORMAT,
                "Invalid base64 file format!"
            )

        return data

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        images_data = validated_data.pop("images", [])
        if user.role == "admin":
            owner = validated_data.pop("owner", None)
            if owner is None:
                raise_error(
                    ErrorCodes.FIELD_REQUIRED,
                    "This field is required for admins."
                )
        else:
            owner = user

        field = Field.objects.create(owner=owner, **validated_data)

        image_urls = []
        for base64_image in images_data:
            if base64_image and isinstance(base64_image, str) and check_is_base64(base64_image):
                image_url = base64_to_file(base64_image, name='image', folder='images')
                if image_url:
                    image_urls.append(image_url)

        field.images = image_urls
        field.save()
        return field


class FieldUpdateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Field
        fields = [
            'owner',
            'name',
            'address',
            'contact',
            'price_per_hour',
            'latitude',
            'longitude',
            'images',
        ]

    def validate(self, data):
        images = data.get('images', getattr(self.instance, 'images', None))

        if images and not check_is_base64(images):
            raise_error(
                ErrorCodes.INVALID_FILE_FORMAT,
                "Invalid base64 file format!"
            )

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user
        images_data = validated_data.pop("images", None)

        if user.role == "admin" and 'owner' in validated_data:
            instance.owner = validated_data.pop("owner")

        if images_data:
            image_urls = []
            for base64_image in images_data:
                image_url = base64_to_file(base64_image, name='image', folder='images')
                if image_url:
                    image_urls.append(image_url)

            instance.images = image_urls

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class FieldSerializer(serializers.ModelSerializer):
    bookings = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = [
            'id',
            'owner',
            'name',
            'address',
            'contact',
            'price_per_hour',
            'latitude',
            'longitude',
            'images',
            'created_at',
            'bookings'
        ]

    def get_bookings(self, obj):
        bookings = obj.bookings.all().values('id', 'start_time', 'end_time', 'user__full_name')
        return bookings
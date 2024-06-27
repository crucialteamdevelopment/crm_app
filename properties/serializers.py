from rest_framework import serializers
from .models import Property, PropertyType, PropertyUnit, PropertyImage

from PIL import Image

class PropertyImageSerializer(serializers.ModelSerializer):
    MAX_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB

    def validate_image(self, value):
        if value.size > self.MAX_SIZE_BYTES:
            raise serializers.ValidationError("The image file size should not exceed 2 MB.")
        
        try:
            img = Image.open(value)
            img.verify()  # Проверка на целостность файла
        except:
            raise serializers.ValidationError("Invalid image file.")
        
        accepted_formats = ['JPEG', 'PNG']  # Поддерживаемые форматы
        if img.format not in accepted_formats:
            raise serializers.ValidationError(f"Unsupported image format. Accepted formats: {accepted_formats}.")
        
        return value

    class Meta:
        model = PropertyImage
        fields = ['id', 'property', 'image', 'description']
        read_only_fields = ['id', 'property']

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class PropertyUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyUnit
        fields = ['id', 'name', 'description', 'type', 'property', 'location', 'size', 'price', 'is_available', 'date_added']
        read_only_fields = ['id', 'date_added']

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    units = PropertyUnitSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'street_address', 'zip_code', 'state', 'city', 'neighborhood', 
            'building_name', 'number_of_floors', 'holding_company', 'property_type', 
            'owner', 'images', 'units'
        ]
        read_only_fields = ['id', 'owner']

class CreatePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'street_address', 'zip_code', 'state', 'city', 'neighborhood', 
            'building_name', 'number_of_floors', 'holding_company', 'property_type', 
            'owner'
        ]
        read_only_fields = ['id', 'owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

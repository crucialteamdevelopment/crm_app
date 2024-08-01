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
    property_type = PropertyTypeSerializer()  # Вложенный сериализатор для чтения

    class Meta:
        model = Property
        fields = [
            'id', 'street_address', 'zip_code', 'state', 'city', 'neighborhood', 
            'building_name', 'number_of_floors', 'holding_company', 'property_type', 
            'owner', 'images', 'units', 'status'
        ]
        read_only_fields = ['id', 'owner']

    def update(self, instance, validated_data):
        property_type_data = validated_data.pop('property_type', None)
        
        # Обновляем поля модели
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Обновляем вложенные данные
        if property_type_data:
            property_type_name = property_type_data.get('name')
            if property_type_name:
                property_type, created = PropertyType.objects.get_or_create(name=property_type_name)
                instance.property_type = property_type

        instance.save()
        return instance


class CreatePropertySerializer(serializers.ModelSerializer):
    property_type = serializers.CharField()

    class Meta:
        model = Property
        fields = [
            'street_address', 'zip_code', 'state', 'city', 'neighborhood', 
            'building_name', 'number_of_floors', 'holding_company', 'property_type', 
            'owner', 'status'
        ]
        read_only_fields = ['id', 'owner']

    def create(self, validated_data):
        property_type_name = validated_data.pop('property_type')

        # Проверяем наличие property_type в базе данных
        property_type, created = PropertyType.objects.get_or_create(name=property_type_name)

        validated_data['owner'] = self.context['request'].user
        validated_data['property_type'] = property_type

        return super().create(validated_data)

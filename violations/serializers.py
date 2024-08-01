from rest_framework import serializers
from .models import Violation, Field

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'
        extra_kwargs = {
            'violation': {'required': False},
        }

class ViolationSerializer(serializers.ModelSerializer):
    additional_fields = FieldSerializer(many=True, required=False)

    class Meta:
        model = Violation
        fields = '__all__'

    def create(self, validated_data):
        additional_fields_data = validated_data.pop('additional_fields', [])
        violation = Violation.objects.create(**validated_data)
        for field_data in additional_fields_data:
            Field.objects.create(violation=violation, **field_data)
        return violation

def update(self, instance, validated_data):
    # Извлечение данных дополнительных полей
    additional_fields_data = validated_data.pop('additional_fields', [])
    
    # Обновление полей модели Violation
    instance.violation_number = validated_data.get('violation_number', instance.violation_number)
    instance.issuing_agency = validated_data.get('issuing_agency', instance.issuing_agency)
    instance.agency_violation_number = validated_data.get('agency_violation_number', instance.agency_violation_number)
    instance.issued_to = validated_data.get('issued_to', instance.issued_to)
    instance.severity = validated_data.get('severity', instance.severity)
    instance.status = validated_data.get('status', instance.status)
    instance.standard_penalty = validated_data.get('standard_penalty', instance.standard_penalty)
    instance.maximum_penalty = validated_data.get('maximum_penalty', instance.maximum_penalty)
    instance.face_amount = validated_data.get('face_amount', instance.face_amount)
    instance.balance = validated_data.get('balance', instance.balance)
    instance.court_decision = validated_data.get('court_decision', instance.court_decision)
    instance.government_link = validated_data.get('government_link', instance.government_link)
    instance.save()

    # Обновление или создание дополнительных полей
    existing_field_ids = [field.id for field in instance.additional_fields.all()]
    new_field_ids = []

    for field_data in additional_fields_data:
        field_id = field_data.get('id')
        if field_id:
            if field_id in existing_field_ids:
                # Обновление существующего поля
                field = Field.objects.get(id=field_id, violation=instance)
                field.name = field_data.get('name', field.name)
                field.value = field_data.get('value', field.value)
                field.save()
                new_field_ids.append(field_id)
            else:
                # Если ID не существует, игнорируем, чтобы избежать дублирования
                continue
        else:
            # Создание нового поля
            Field.objects.create(violation=instance, **field_data)
    
    # Удаление полей, которые больше не присутствуют
    for field_id in existing_field_ids:
        if field_id not in new_field_ids:
            Field.objects.filter(id=field_id, violation=instance).delete()

    return instance


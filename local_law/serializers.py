from rest_framework import serializers
from .models import LocalLaw, LocalLawField, LocalLawDates, LocalLawContacts, LocalLawNote

class LocalLawSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalLaw
        fields = '__all__'

class LocalLawFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalLawField
        fields = '__all__'

class LocalLawDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalLawDates
        fields = '__all__'

class LocalLawContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalLawContacts
        fields = '__all__'

class LocalLawNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalLawNote
        fields = '__all__'

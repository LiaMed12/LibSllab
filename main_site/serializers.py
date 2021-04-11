from rest_framework import serializers

from .models import specifications


class SpecifSerializers(serializers.ModelSerializer):
    class Meta:
        model = specifications
        fields = '__all__'


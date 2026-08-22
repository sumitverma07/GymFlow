from rest_framework import serializers

from .models import ExerciseImage


class ExerciseImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseImage
        fields = '__all__'

class ExerciseImageBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseImage
        fields = [
            'id',
            'image_url',   
        ]
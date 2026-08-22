from rest_framework import serializers
from categories.serializers import CategoryBasicSerializer
from exercise_images.serializers import ExerciseImageBasicSerializer
from .models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = '__all__'

class ExerciseBasicSerializer(serializers.ModelSerializer):
    category=CategoryBasicSerializer()
    images=serializers.SerializerMethodField()
    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
            'body_part',
            'primary_muscle',
            'category',
            'images'   
        ]
    

    def get_images(self,obj):
        images= obj.exercise_images_exercise.all()
        return ExerciseImageBasicSerializer(images, many=True).data

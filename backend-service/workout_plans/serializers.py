from rest_framework import serializers

from .models import WorkoutPlan
from exercises.models import Exercise


class WorkoutPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutPlan
        fields = ["id", "name", "day"]


class WorkoutPlanBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = ["id", "name", "day"]


class WorkoutExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    exercise_ids = serializers.ListField(child=serializers.IntegerField())

    def validate(self, attrs):
        id = attrs.get("id")
        exercise_ids = attrs.get("exercise_ids")
        try:
            wk = WorkoutPlan.objects.get(id=id)
        except WorkoutPlan.DoesNotExist:
            raise serializers.ValidationError({"message": "bhag guji"})

        valid_exercises = Exercise.objects.filter(id__in=exercise_ids)
        valid_ids = set(valid_exercises.values_list("id", flat=True))
        print("valid ids ", valid_ids)
        invalid_ids = set(exercise_ids) - valid_ids
        print("inv ", invalid_ids)
        print("hey ", valid_exercises)
        if not valid_ids:
            raise serializers.ValidationError(
                {"message": "No valid exercise IDs provided"}
            )
        if invalid_ids:
            raise serializers.ValidationError(
                {"message": f"Invalid exercise IDs: {sorted(invalid_ids)}"}
            )
        attrs["wk"] = wk
        attrs["valid_ids"] = valid_ids
        return super().validate(attrs)

    def create(self, validated_data):
        wk = validated_data.get("wk")
        exercise_ids = validated_data.get("valid_ids")
        wk.exercises.add(*exercise_ids)

        return validated_data

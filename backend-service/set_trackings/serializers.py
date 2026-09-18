from rest_framework import serializers

from .models import SetTracking
from performed_workouts.models import PerformedWorkout
from exercises.models import Exercise


class SetTrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = SetTracking
        fields = "__all__"


class SetTrackingBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetTracking
        fields = ["id", "set_number", "reps", "weight"]


# class SetSerilizer(serializers.ModelSerializer):
#     exercises = ExeS()

#     class Meta:
#         model = SetTracking
#         fields = ["exercises"]


class RecordSetSerializer(serializers.Serializer):
    performed_workout_id = serializers.IntegerField()
    exercise_id = serializers.IntegerField()
    set_no = serializers.IntegerField()
    reps = serializers.IntegerField()
    weight = serializers.IntegerField()

    def validate(self, attrs):
        performed_workout_id = attrs.get("performed_workout_id")
        exercise_id = attrs.get("exercise_id")
        try:
            pw = PerformedWorkout.objects.get(id=performed_workout_id)
        except PerformedWorkout.DoesNotExist:
            raise serializers.ValidationError({"ok": "Invalid performed_workout_id"})
        try:
            e_id = Exercise.objects.get(id=exercise_id)
        except Exercise.DoesNotExist:
            raise serializers.ValidationError({"ok": "Invalid exercise_id"})
        attrs["pw"] = pw
        attrs["e_id"] = e_id
        return super().validate(attrs)

    def create(self, validated_data):
        pw = validated_data.get("pw")
        e_id = validated_data.get("e_id")
        set_no = validated_data.get("set_no")
        reps = validated_data.get("reps")
        weight = validated_data.get("weight")
        SetTracking.objects.create(
            performed_workout=pw,
            exercise=e_id,
            set_number=set_no,
            reps=reps,
            weight=weight,
        )
        return validated_data

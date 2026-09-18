from rest_framework import serializers
from workout_plans.serializers import WorkoutPlanBasicSerializer

from .models import PerformedWorkout
from django.db import connection


class PerformedWorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerformedWorkout
        fields = "__all__"


class PerformedWorkoutBasicSerializer(serializers.ModelSerializer):
    workout_plan = WorkoutPlanBasicSerializer()

    class Meta:
        model = PerformedWorkout
        fields = ["id", "performed_at", "workout_plan", "notes"]


class PerformedWorkoutDetailSerializer(serializers.ModelSerializer):
    exercises = serializers.SerializerMethodField()

    class Meta:
        model = PerformedWorkout
        fields = ["id", "performed_at", "exercises"]

    def get_exercises(self, obj):
        set_trackings = obj.set_trackings

        exercises = {}
        for set_tracking in set_trackings:
            exercise = set_tracking.exercise
            print("after ", len(connection.queries))
            if exercise.id not in exercises:
                exercises[exercise.id] = {
                    "exercise_id": exercise.id,
                    "exercise_name": exercise.name,
                    "sets": [],
                }
            exercises[exercise.id]["sets"].append(
                {
                    "set_no": set_tracking.set_number,
                    "reps": set_tracking.reps,
                    "weight": set_tracking.weight,
                }
            )
        return exercises.values()

from django.contrib.auth.models import User
from django.db import models
from profiles.models import Profile
from workout_plans.models import WorkoutPlan

# To log events of the application
from simple_history.models import HistoricalRecords

# Create your models here.


class PerformedWorkout(models.Model):
    # Relations
    created_by = models.ForeignKey(
        User,
        null=True,
        related_name="performed_workout_creator",
        blank=True,
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        related_name="performed_workout_updater",
        blank=True,
        on_delete=models.CASCADE,
    )
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="performed_workout_profile",
    )

    workout_plan = models.ForeignKey(
        WorkoutPlan,
        null=True,
        on_delete=models.CASCADE,
        related_name="performed_workouts",
        blank=True,
    )

    performed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    archive = models.BooleanField(default=False, null=True, blank=True)

    date_created = models.DateField(auto_created=True, auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    # for recording history
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.updated_by

    @_history_user.setter
    def _history_user(self, value):
        self.updated_by = value

    def __str__(self):
        return f"PerformedWorkout {self.id}"

    # Custom save method
    def save(self, *args, **kwargs):
        super(PerformedWorkout, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-id"]

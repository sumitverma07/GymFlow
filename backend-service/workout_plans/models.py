from django.contrib.auth.models import User
from django.db import models
from profiles.models import Profile
from exercises.models import Exercise

# To log events of the application
from simple_history.models import HistoricalRecords

# Create your models here.


class WorkoutPlan(models.Model):
    class DayChoices(models.TextChoices):
        MONDAY = "Monday", "Monday"
        TUESDAY = "Tuesday", "Tuesday"
        WEDNESDAY = "Wednesday", "Wednesday"
        THURSDAY = "Thursday", "Thursday"
        FRIDAY = "Friday", "Friday"
        SATURDAY = "Saturday", "Saturday"

    # Relations
    profile = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.CASCADE,
        related_name="workout_plan_profile",
        blank=True,
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        related_name="workout_plan_creator",
        blank=True,
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        related_name="workout_plan_updater",
        blank=True,
        on_delete=models.CASCADE,
    )
    exercises = models.ManyToManyField(
        Exercise, related_name="workout_plan_exercises", blank=True
    )

    name = models.CharField(max_length=100)
    day = models.CharField(max_length=20, choices=DayChoices.choices)
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
        return self.name

    # Custom save method
    def save(self, *args, **kwargs):
        super(WorkoutPlan, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-id"]

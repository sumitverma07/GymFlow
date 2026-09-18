from django.contrib.auth.models import User
from django.db import models
from exercises.models import Exercise
from performed_workouts.models import PerformedWorkout

# To log events of the application
from simple_history.models import HistoricalRecords

# Create your models here.


class SetTracking(models.Model):
    # Relations
    created_by = models.ForeignKey(
        User,
        null=True,
        related_name="set_tracking_creator",
        blank=True,
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        related_name="set_tracking_updater",
        blank=True,
        on_delete=models.CASCADE,
    )
    performed_workout = models.ForeignKey(
        PerformedWorkout,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="set_tracking_performed_workout",
    )
    exercise = models.ForeignKey(
        Exercise,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="set_tracking_exercise",
    )

    set_number = models.IntegerField(default=1)
    reps = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
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
        return f"Set {self.set_number} - {self.reps} reps @ {self.weight}"

    # Custom save method
    def save(self, *args, **kwargs):
        super(SetTracking, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-id"]

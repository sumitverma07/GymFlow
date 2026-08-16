from django.contrib.auth.models import User
from django.db import models
from categories.models import Category

#To log events of the application
from simple_history.models import HistoricalRecords

# Create your models here.


class Exercise(models.Model):
    BODY_PART_CHOICES = [
    ('CHEST', 'Chest'),
    ('BACK', 'Back'),
    ('ARMS', 'Arms'),
    ('LEGS', 'Legs'),
    ('SHOULDERS', 'Shoulders'),
    ('CORE', 'Core'),
    ('NECK', 'Neck'),
    ]

    PRIMARY_MUSCLE_CHOICES = [
        # Chest
        ('CHEST', 'Chest'),

        # Back
        ('LATS', 'Lats'),
        ('MIDDLE_BACK', 'Middle Back'),
        ('LOWER_BACK', 'Lower Back'),
        ('TRAPS', 'Traps'),

        # Arms
        ('BICEPS', 'Biceps'),
        ('TRICEPS', 'Triceps'),
        ('FOREARMS', 'Forearms'),

        # Legs
        ('QUADRICEPS', 'Quadriceps'),
        ('HAMSTRINGS', 'Hamstrings'),
        ('GLUTES', 'Glutes'),
        ('CALVES', 'Calves'),
        ('ABDUCTORS', 'Abductors'),
        ('ADDUCTORS', 'Adductors'),

        # Shoulders
        ('SHOULDERS', 'Shoulders'),

        # Core
        ('ABDOMINALS', 'Abdominals'),

        # Neck
        ('NECK', 'Neck'),
    ]

    #Relations
    created_by = models.ForeignKey(
        User, 
        null=True,
        related_name='exercise_creator',
        blank=True, 
        on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User, 
        null=True, 
        related_name='exercise_updater',
        blank=True, 
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    body_part = models.CharField(
        max_length=100,
        choices=BODY_PART_CHOICES
    )
    primary_muscle = models.CharField(
        max_length=100,
        choices=PRIMARY_MUSCLE_CHOICES
    )

    instructions = models.TextField(blank=True)
    
    archive = models.BooleanField(default=False, null=True, blank=True)

    date_created = models.DateField(auto_created=True, auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    #for recording history
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
        super(Exercise, self).save(*args, **kwargs)   

    class Meta:
        ordering = ['-id']
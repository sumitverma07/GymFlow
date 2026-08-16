from django.contrib.auth.models import User
from django.db import models

#To log events of the application
from simple_history.models import HistoricalRecords

# Create your models here.


class Category(models.Model):

    #Relations
    created_by = models.ForeignKey(
        User, 
        null=True,
        related_name='category_creator',
        blank=True, 
        on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User, 
        null=True, 
        related_name='category_updater',
        blank=True, 
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    
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
        super(Category, self).save(*args, **kwargs)   

    class Meta:
        ordering = ['-id']
from django.contrib.auth.models import User
from django.db import models

#To log events of the application
from simple_history.models import HistoricalRecords

# Create your models here.


class Profile(models.Model):
    #Relations
    created_by = models.ForeignKey(
        User, 
        null=True,
        related_name='profile_creator',
        blank=True, 
        on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User, 
        null=True, 
        related_name='profile_updater',
        blank=True, 
        on_delete=models.CASCADE
    )
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
    )

    phone_no = models.CharField(max_length=255)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
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
        return self.phone_no

    # Custom save method
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)    

    class Meta:
        ordering = ['-id']
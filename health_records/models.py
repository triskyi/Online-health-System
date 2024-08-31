from django.db import models
from users.models import CustomUser  # Adjust the import if necessary

class HealthRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Allows multiple records per user
    insurance_details = models.CharField(max_length=255)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    age = models.PositiveIntegerField(default=0)  # Added age field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HealthRecord for {self.user.username} (ID: {self.id})"

from django.db import models

# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField()
    case_number = models.CharField(max_length=23)

    def __str__(self):
        return f"{self.email} - {self.case_number}"
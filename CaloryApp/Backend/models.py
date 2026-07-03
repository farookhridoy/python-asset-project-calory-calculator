from django.db import models
from django.contrib.auth.models import User

class CalorieProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")

    def bmr(self):
        if self.gender == 'Male':
            return 66.47 + (13.75 * self.weight) + (5.003 * self.height) - (6.755 * self.age)
        else:
            return 655.1 + (9.563 * self.weight) + (1.850 * self.height) - (4.676 * self.age)

    def __str__(self):
        return self.name

class FoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    calories = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.item_name} - {self.calories}cal"

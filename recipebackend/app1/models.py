from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Recipe(models.Model):
    r_name=models.CharField(max_length=20)
    r_ingredients=models.CharField(max_length=50)
    instruction=models.TextField()
    r_cusine=models.CharField(max_length=20)
    meal_type=models.CharField(max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='media/images',null=True,blank=True)

    def __str__(self):
        return self.r_name
from django.contrib.auth.models import User
class Review(models.Model):
    recipe=models.ForeignKey(Recipe,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField()
    rating=models.IntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



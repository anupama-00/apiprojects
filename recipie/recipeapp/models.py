from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Recipe(models.Model):
    recipe_name=models.CharField(max_length=30)
    recipe_ingredient=models.CharField(max_length=50)
    instructions=models.TextField()
    recipe_cuisine=models.CharField(max_length=30)
    meal_type=models.CharField(max_length=30)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='images')

    def __str__(self):
        return self.recipe_name

class Review(models.Model):
    recipe=models.ForeignKey(Recipe,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comments=models.TextField()
    rating=models.IntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipe.recipe_name
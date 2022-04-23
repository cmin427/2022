from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=10)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    곡물전분류 = models.IntegerField(default=0)
    김치류 = models.IntegerField(default=0)
    난류 = models.IntegerField(default=0)
    면류 = models.IntegerField(default=0)
    버섯류 = models.IntegerField(default=0)
    유제품 = models.IntegerField(default=0)
    육류 = models.IntegerField(default=0)
    조리가공품류 = models.IntegerField(default=0)
    채소류 = models.IntegerField(default=0)
    해산물 = models.IntegerField(default=0)
    기타 = models.IntegerField(default=0)
    조미료 = models.IntegerField(default=0)
    견과류 = models.IntegerField(default=0)

class user_history(models.Model):
    user_num = models.IntegerField(default=-1)
    food_1 = models.CharField(max_length=500,default='f')
    food_2 = models.CharField(max_length=500,default='-1')
    food_3 = models.IntegerField(default=-1)
    food_4 = models.IntegerField(default=-1)
    food_5 = models.IntegerField(default=-1)
    food_6 = models.IntegerField(default=-1)
    food_7 = models.IntegerField(default=-1)

class foodmodel(models.Model):
    recipe_title = models.CharField(max_length=100) 
    raw_ingre = models.TextField()
    main_ingredients = models.TextField()
    ingredients = models.TextField()
    steps = models.TextField()
    method_type = models.TextField()
    cook_time = models.TextField()
    difficult = models.TextField()
    kcal = models.TextField()
    feature = models.TextField()
    raw_ingre_sep = models.TextField()

    def __str__(self):
        return f'{self.recipe_title}: {self.raw_ingre}'
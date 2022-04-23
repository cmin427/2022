from django.contrib import admin
from .models import User,foodmodel,user_history


# Register your models here.

admin.site.register(User)
admin.site.register(foodmodel)
admin.site.register(user_history)
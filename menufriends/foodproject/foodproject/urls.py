"""foodproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from foodapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('index/',views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recipe1/', views.recipe1, name='recipe1'),
    path('recipe_1/<int:menu_index>/<int:Users_pk>/', views.recipe_1, name='recipe_1'),
    path('recipe_2/', views.recipe_2, name='recipe_2'),
    path('recipe_3/', views.recipe_3, name='recipe_3'),
    path('recipe_4/', views.recipe_4, name='recipe_4'),
    path('recipe_5/', views.recipe_5, name='recipe_5'),
    path('recommend/<int:User_pk>', views.recommend, name='recommend'),
    path('pay/<int:User_pk>', views.pay, name='pay'),
]

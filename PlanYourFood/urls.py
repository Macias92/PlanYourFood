"""PlanYourFood URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from jedzonko.views import IndexView, DashboardView, RecipeListView, RecipeDetailsView, AddRecipeView,RecipeIdModifyView, \
    PlanIdView, PlanAddView, PlanAddNewRecipeView, PlanListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('main/', DashboardView.as_view()),
    path('recipe/<int:id>/', RecipeDetailsView.as_view()),
    path('recipe/<int:id>/', RecipeDetailsView.as_view(), name='recipe_details'),
    path('recipe/add/', AddRecipeView.as_view(), name='add_recipe'),
    path('recipe/modify/<int:id>/', RecipeIdModifyView.as_view(), name='recipe_modify'),
    path('plan/<int:id>/', PlanIdView.as_view(), name='plan'),
    path('plan/add/', PlanAddView.as_view(), name='add_plan'),
    path('plan/add-recipe/',PlanAddNewRecipeView.as_view(), name='plan_add_recipe'),
    path('plan/list/',PlanListView.as_view(), name='plan_list'),
    path('recipe/list/', RecipeListView.as_view(), name="recipes"),

]

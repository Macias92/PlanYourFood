from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from jedzonko.models import Recipe, Plan, DAYS_NAMES, DayName, RecipePlan
from random import sample


class IndexView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        list_recipes = sample(list(map(lambda x: x, recipes)), 3)
        ctx = {"actual_date": datetime.now(), "list_recipes": list_recipes}
        return render(request, "index.html", ctx)


class DashboardView(View):
    def get(self, request):
        latest_plan = Plan.objects.all().order_by('-created')[0]
        plan_details = latest_plan.recipeplan_set.all().order_by('order')
        plan_recipes = []
        plans_total = Plan.objects.count()
        recipes_total = Recipe.objects.count()
        for i in range(1, 8):
            recipes = plan_details.filter(day_name__order=i)
            if len(recipes) > 0:
                plan_recipes.append((recipes[0].day_name.name, recipes))
        return render(request, "dashboard.html", context={'latest_plan': latest_plan,
                                                          'DAYS_NAMES': DAYS_NAMES,
                                                          'plan_recipes': plan_recipes,
                                                          'plans_total': plans_total,
                                                          'recipes_total': recipes_total})


class RecipeIdModifyView(View):
    def get(self, request, id):
        return render(request, 'app-edit-recipe.html')


class PlanIdView(View):
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        recipe_plan = plan.recipeplan_set.all().order_by('order')
        day_and_meals = []
        for i in range(1, 8):
            recipes_for_day = recipe_plan.filter(day_name__order=i)
            if len(recipes_for_day) > 0:
                day_and_meals.append((recipes_for_day[0].day_name, recipes_for_day))
        context = {
            'plan': plan,
            'day_and_meals': day_and_meals,
            'days_names': DAYS_NAMES
                   }
        return render(request, 'app-details-schedules.html', context)


class PlanAddView(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        errors = []
        plan_name = request.POST.get("planName")
        plan_description = request.POST.get("planDescription")
        if not (plan_name and plan_description):
            errors.append("Wypełnij poprawnie wszystkie pola!!!")
        if len(errors) == 0:
            plan = Plan.objects.create(name=plan_name, description=plan_description)
            id = plan.id
            return redirect(f'/plan/{id}')
        return render(request, 'app-add-schedules.html', context={'errors': errors})


class PlanAddNewRecipeView(View):
    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.objects.all()
        context = {'plans': plans, 'recipes': recipes, 'days': days}
        return render(request, 'app-schedules-meal-recipe.html', context)

    def post(self, request):
        plan_id = request.POST.get('plan')
        meal_name = request.POST.get('meal_name')
        order = request.POST.get('order_number')
        recipe_id = request.POST.get('recipe')
        day_name_id = request.POST.get('day_name')
        RecipePlan.objects.create(plan_id=plan_id, meal_name=meal_name, order=order, recipe_id=recipe_id,
                                  day_name_id=day_name_id)

        return redirect(f'/plan/{plan_id}')


class PlanListView(View):
    def get(self, request):
        plans = Plan.objects.all().order_by('name')
        i = 0
        for plan in plans:
            plan.id_counter = i + 1
            i += 1
        paginator = Paginator(plans, 2)  # paginacja testowo na 2 plany na stronę
        page_number = request.GET.get('page')
        page_obj = paginator.get_page((page_number))
        return render(request, 'app-schedules.html', context={'page_obj': page_obj})

      
class RecipeListView(View):
    def get(self, request):
        recipes = Recipe.objects.all().order_by('-created').order_by('-votes')
        i = 0
        for recipe in recipes:
            recipe.id_counter = i + 1
            i += 1
        paginator = Paginator(recipes, 2) # paginacja testowo na 2 przepisy na stronę
        page_number = request.GET.get('page')
        page_obj = paginator.get_page((page_number))
        return render(request, 'app-recipes.html', context={'page_obj': page_obj})


class RecipesView(View):
    def get(self, request):
        return render(request, 'app-recipes.html')


class RecipeDetailsView(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        return render(request, 'app-recipe-details.html', {'recipe': recipe})
    def post(self, request, id):
        recipe = Recipe.objects.get(id=id)
        recipe.votes += 1
        recipe.save()
        return redirect(f'/recipe/{recipe.id}')
        

class AddRecipeView(View):
    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        errors = []
        name = request.POST.get("name")
        preparation_time = request.POST.get("preparation_time")
        ingredients = request.POST.get("ingredients")
        description = request.POST.get("description")

        if not (name and preparation_time and ingredients and description):
            errors.append("Wypełnij poprawnie wszystkie pola!!!")

        if len(errors) == 0:
            recipe = Recipe.objects.create(name=name, preparation_time=preparation_time, ingredients=ingredients,
                                           description=description)
            return redirect('recipes')
        return render(request, 'app-add-recipe.html', context={'errors': errors})

from enum import Enum
from django.db import models


DAYS_NAMES = (
    ('PN', 'Poniedziałek'),
    ('WT', 'Wtorek'),
    ('SR', 'Środa'),
    ('CZW', 'Czwartek'),
    ('PT', 'Piątek'),
    ('SB', 'Sobota'),
    ('ND', 'Niedziela')
)


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through="RecipePlan")


# class DayNamesChoice(Enum): # enum: https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63
#     PN = 'Poniedziałek'
#     WT = 'Wtorek'
#     SR = 'Środa'
#     CZW = 'Czwartek'
#     PT = 'Piątek'
#     SB = 'Sobota'
#     ND = 'Niedziela'


class DayName(models.Model):
    # name = models.CharField(max_length=16, choices=[(tag, tag.value) for tag in DayNamesChoice])
    name = models.CharField(max_length=16, choices=DAYS_NAMES)
    order = models.IntegerField(unique=True)


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)


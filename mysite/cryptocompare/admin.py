from django.contrib import admin
from .models import Portfolio

admin.site.register(Portfolio)

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("id", "coin_name")


# Register your models here.

from django.contrib import admin
from .models import Business, Store, Pack, Game, PackUpdate

# Register your models here.

admin.site.register([Business, Store, Pack, Game, PackUpdate])
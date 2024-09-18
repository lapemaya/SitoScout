from django.contrib import admin

# Register your models here.

from .models import Conto,Spesa

admin.site.register(Conto)
admin.site.register(Spesa)
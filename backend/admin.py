from django.contrib import admin
from .models import Pass, Provider, Station, Vehicle

# Register your models here.
admin.site.register(Pass)
admin.site.register(Provider)
admin.site.register(Station)
admin.site.register(Vehicle)
from django.contrib import admin
from .models import Persona, Producto, Genero, Usuario

# Register your models here.
admin.site.register(Producto)
admin.site.register(Persona)
admin.site.register(Genero)
admin.site.register(Usuario)
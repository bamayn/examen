from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.shortcuts import render
from .carro import Carro
from app.models import Producto
from django.shortcuts import redirect

# Create your views here.

def eliminar_producto(request, idProducto):
    carro = Carro(request)
    producto = Producto.objects.get(idProducto=idProducto)
    carro.eliminar(producto=producto)
    return redirect("carro")


def restar_producto(request, idProducto):
    carro = Carro(request)
    producto = Producto.objects.get(idProducto=idProducto)
    carro.restar_producto(producto=producto)
    return redirect("carro")

def agregar_producto(request, idProducto):
    carro = Carro(request)
    producto = Producto.objects.get(idProducto=idProducto)
    carro.agregar(producto=producto)
    return redirect("carro")


def limpiar_carro(request, idProducto):
    carro = Carro(request)
    carro.vaciar_carro()
    return redirect("carro")

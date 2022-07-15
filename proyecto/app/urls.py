from django.urls import path, include
from . import views
from django.urls import path, include
from . import views

from .views import ProductoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('producto', ProductoViewSet)

urlpatterns =[
    path('',views.index,name='index'),

    path('login/',views.login,name='login'),
    path('tienda/',views.tienda,name='tienda'),
    path('crud/',views.crud,name='crud'),
    path('producto_det/<str:pk>', views.producto_detalle, name='producto_det'),
    path('carro/',views.carrito,name='carro'),
    path('registro/',views.registro,name='registro'),
    path('productos_del/<str:pk>', views.productos_del, name='productos_del'),
    path('productos_edit/<str:pk>', views.productos_edit, name='productos_edit'),
    path("productosAdd", views.productosAdd, name="productosAdd" ),
    path('usuarios/',views.usuarios,name='usuarios'),
    path('del_usuario/<str:pk>', views.del_usuario, name='del_usuario'),
    path('editar_usuario/<str:pk>', views.editar_usuario, name='editar_usuario'),
    path('cargar_formulario_usuario', views.cargar_formulario_usuario, name='cargar_formulario_usuario'),
    path('comprar/',views.comprar,name="comprar"),
    path('mi_venta/',views.mi_venta,name="mi_venta"),
    path('pedidos/',views.pedidos,name="pedidos"),
    path('editar_pedido/<int:pk>', views.editar_pedido, name='editar_pedido'),
    path('api/', include(router.urls)),
]
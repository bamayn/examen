from django.shortcuts import get_object_or_404, redirect, render

from .models import Producto,Usuario,Venta,DetalleVenta
from carro.carro import Carro
from . forms import Usuario as FormUsuario
from .forms import VentaForm
from .forms import usuarioRegistro,usuarioEdit
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import ProductoSerializer

# Create your views here.


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

def index(request):
    print("Estoy en index")
    context={}
    return render(request,'app/index.html',context)

def login(request):
    print("Estoy en login")
    usuarios = Usuario.objects.all()
    context={"usuarios":usuarios}
    return render(request,'app/login.html',context)

def registro(request):
    data ={ 
        'form':usuarioRegistro()
    }

    if request.method == 'POST':
        formulario = usuarioRegistro(data = request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            auth_login(request, user)
            return redirect(to='index')
        data["form"] = formulario


    return render(request, 'registration/registro.html',data)

def home(request):
    print("Estoy en home")
    context={}
    return render(request,'app/home.html',context)

def tienda(request):
    print("Estoy en tienda")
    productos = Producto.objects.all()
    context={"productos":productos}
    return render(request,'app/tienda.html',context)

def crud(request):
    print("Estoy en crud")
    productos = Producto.objects.all()
    context={"productos":productos}
    return render(request,'app/crud.html',context)

def carrito(request):
    context={}
    return render(request,'app/carro.html',context)

def producto_detalle(request, pk):
    producto = Producto.objects.get(idProducto=pk)
    context = {
        "producto": producto
    }
    return render(request,'app/producto_det.html',context)

def productosAdd(request):
    print("estoy en controlador ProductosAdd...")
    context={}
    if request.method == "POST":
        print("contralador productos es un post...") 
        opcion=request.POST.get("opcion","")
        print("opcion="+opcion)
        #Listar
        if opcion=="Editar" or opcion == "Volver":
            productos = Producto.objects.all()
            context ={'productos':productos}
            print("enviando datos a productos_list")
            return render(request,"app/crud.html",context) 
        #Agregar
        if opcion=="Agregar":
            idProducto=request.POST["idProducto"]
            nombreProducto=request.POST["nombreProducto"]
            stock=int(request.POST["stock"])
            precio=int(request.POST["precio"])
            foto=request.FILES["foto"]

       
            if idProducto != "" and nombreProducto != "" and stock >=0 and precio >=0:

                producto = Producto(idProducto, nombreProducto, stock, precio,
                                    foto) 
                producto.save()
                context={'mensaje':"Ok, datos grabados..."}
                redirect('crud')
            else:
                context={'mensaje':"Error, los campos no deben estar vacios"}

           #Agregar
        if opcion=="Actualizar":
            idProducto=request.POST["idProducto"]
            nombreProducto=request.POST["nombreProducto"]
            stock=int(request.POST["stock"])
            precio=int(request.POST["precio"])
            try:
                foto=request.FILES["foto"]
            except:
                foto=""
       
            if idProducto != "" and nombreProducto != "" and stock >=0 \
                and precio >=0:

                producto = Producto(idProducto, nombreProducto, stock, precio,
                                    foto) 
                producto.save()
                context={'mensaje':"Ok, datos grabados..."}
            else:
                context={'mensaje':"Error, los campos no deben estar vacios"}
            return render(request,"app/productos_edit.html",context) 


    return render(request,"app/agregar_producto.html",context)   

def productos_del(request, pk):
    mensajes=[]
    errores=[]
    productos = Producto.objects.all()
    try:
        producto=Producto.objects.get(idProducto=pk)
        context={}
        if producto:
           producto.delete()
           mensajes.append("Bien, datos eliminados...")

           context = {'productos': productos,  'mensajes': mensajes, 'errores':errores}

           return render(request, 'app/crud.html', context)

    except:
        print("Error, producto no existe")
        errores.append("Error producto no encontrado.")
        context = {'productos': productos,  'mensajes': mensajes, 'errores':errores}
        return render(request, 'app/crud.html', context)

def productos_edit(request, pk):
    mensajes=[]
    errores=[]   
    
    context={}
    #productos = Producto.objects.all()
    #try:
    producto=Producto.objects.get(idProducto=pk)

    context={}
    if producto:
        print("Edit encontró a producto...")
        mensajes.append("Bien, datos eliminados...")

        context = {'producto': producto,  'mensajes': mensajes, 'errores':errores}

        return render(request, 'app/productos_edit.html', context)
    
    return render(request, 'app/crud.html', context)

def usuarios(request):
    print("Estoy en crud")
    usuarios = User.objects.all()
    context={"usuarios":usuarios}
    return render(request,'app/usuarios.html',context)

def del_usuario(request, pk):
    mensajes=[]
    errores=[]
    usuarios = Usuario.objects.all()
    try:
        usuario=Usuario.objects.get(rut=pk)
        context={}
        if usuario:
           usuario.delete()
           mensajes.append("Bien, datos eliminados...")
           accion = 'tabla'
           context = {'alumnos': usuarios,  'mensajes': mensajes,'accion':accion, 'errores':errores}
           
           return render(request, 'app/usuarios.html', context)

    except:
        print("Error, eliminar rut no existe")
        errores.append("Error rut no encontrado.")
        context = {'alumnos': usuarios,  'mensajes': mensajes, 'errores':errores}
        return render(request, 'app/usuarios.html', context)

def editar_usuario(request, pk):
    mensajes=[]
    errores=[]
    usuarios = User.objects.all()
    usuario =  get_object_or_404(User, id=pk)

    if usuario:
        form = usuarioEdit(request.POST or None,
                            request.FILES or None, instance=usuario)
        #form = Formalumno(instance=alumno)
        print("estoy en alumno true")
        if request.method == 'POST':
            print("ingresó al POST")
            #form = Formalumno(request.POST, request.FILES)
           # print("formulario id_persona: " + form.id_persona)
            if form.is_valid():
                print("is valid...")
                usuario = form.save()
                usuario.save()
                mensajes.append("Bien!, datos grabados...")
                print("Bien!, datos grabados...")
                accion = 'tabla'
                context = {'usuarios': usuarios, 'mensajes': mensajes,
                           'errores': errores, 'accion': accion}
            else:
                errores.append("Error!, datos no grabados...del EDIT")
                print("Error!, datos no grabados... form="+str(form.errors))
                accion='tabla'
                context = {'usuarios': usuarios, 'mensajes': mensajes,
                       'errores': errores, 'accion': accion}

            return render(request, 'app/usuarios.html', context)
        else:
            mensajes.append("Bien!, id existe...")
            print("entró al else form=alumno()...")
            accion = 'form_edit'
            context = {'usuarios': usuarios, 'mensajes': mensajes,
                       'errores': errores,'form':form, 'accion': accion}
            return render(request, 'app/usuarios.html', context)

    else:
        print("Error, id_alumno no existe")
        errores.append("Error id no encontrado.")
        accion='tabla'
        context = {'usuarios': usuarios, 'mensajes': mensajes,
                   'errores': errores, 'accion':accion}
        return render(request, 'add/usuarios.html', context)

def cargar_formulario_usuario(request):
    context = {}
    mensajes = []
    errores = []
    accion = 'tabla'
    if request.method == 'POST':
        print("Alumno Post")
        form = FormUsuario(request.POST or None, request.FILES or None)
        print("Alumno Post 2")
        if form.is_valid():
            print("Alumno Post is_valid")

            alumno = form.save()
            #alumno.save()
            mensajes.append("Bien!, datos grabados...")
            print("Bien!, datos grabados...")
            alumnos=Usuario.objects.all()
            context = {'form':form, 'mensajes': mensajes,'accion': accion,'usuarios':usuarios}
            return render(request,'app/usuarios.html', context)
        else:
            errores.append( form)
            print("No pasó el is_valid ", form.is_valid())    

    else:
        print("Mostrando formulario alumno...")
        form = FormUsuario()
        accion = 'form_add'

    context = {'form':form, 'mensajes': mensajes,'accion': accion,'errores':errores}
    return render(request,'app/usuarios.html', context)

def comprar(request):

    venta = Venta.objects.create(user=request.user)
    carro = Carro(request)
    productos_venta = list()

    for key,value in carro.carro.items():

        producto = Producto.objects.get(idProducto = key)
        stockVenta = producto.stock - value["cantidad"]

        Producto.objects.filter(idProducto= key).update(stock=stockVenta)
        productos_venta.append(
            DetalleVenta(
                producto_id = producto,
                cantidad=value["cantidad"],
                user = request.user,
                venta_id = venta
            )        
        )

    DetalleVenta.objects.bulk_create(productos_venta)
    carro.vaciar_carro()
    return redirect('tienda')

def mi_venta(request):
    venta = DetalleVenta.objects.filter(user= request.user)
    context={"venta":venta}
    return render(request,'app/mi_venta.html',context)

def pedidos(request):
    print("Estoy en crud")
    pedidos = DetalleVenta.objects.all()
    context={"pedidos":pedidos}
    return render(request,'app/pedidos.html',context)

def editar_pedido(request, pk):
    mensajes=[]
    errores=[]
    ventas = Venta.objects.all()
    venta =  get_object_or_404(Venta, id=pk)

    if venta:
        form = VentaForm(request.POST or None,
                            request.FILES or None, instance=venta)
        #form = Formalumno(instance=alumno)
        print("estoy en venta")
        if request.method == 'POST':
            print("ingresó al POST")
            #form = Formalumno(request.POST, request.FILES)
           # print("formulario id_persona: " + form.id_persona)
            if form.is_valid():
                print("is valid...")
                venta = form.save()
                venta.save()
                mensajes.append("Bien!, datos grabados...")
                print("Bien!, datos grabados...")
                accion = 'tabla'
                context = {'ventas': ventas, 'mensajes': mensajes,
                           'errores': errores, 'accion': accion}
            else:
                errores.append("Error!, datos no grabados...del EDIT")
                print("Error!, datos no grabados... form="+str(form.errors))
                accion='tabla'
                context = {'ventas': ventas, 'mensajes': mensajes,
                       'errores': errores, 'accion': accion}

            return render(request, 'app/pedidos.html', context)
        else:
            mensajes.append("Bien!, id existe...")
            print("entró al else form=alumno()...")
            accion = 'form_edit'
            context = {'ventas': ventas, 'mensajes': mensajes,
                       'errores': errores,'form':form, 'accion': accion}
            return render(request, 'app/pedidos.html', context)

    else:
        print("Error, id_alumno no existe")
        errores.append("Error id no encontrado.")
        accion='tabla'
        context = {'ventas': ventas, 'mensajes': mensajes,
                   'errores': errores, 'accion':accion}
        return render(request, 'app/pedidos.html', context)
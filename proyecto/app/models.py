from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


def cargarFotoProducto(instance, filename):
    return "fotos/foto_{0}_{1}".format(instance.idProducto,filename)

def cargarFoto(instance, filename):
    return "perfil/foto_{0}_{1}".format(instance.rut, filename )


class Producto(models.Model):
    idProducto = models.CharField(max_length=5, primary_key=True)
    nombreProducto = models.CharField(max_length=30, blank=True, null=True)
    stock   = models.IntegerField(blank=True, null=True)
    precio   = models.IntegerField(blank=True, null=True)
    foto = models.ImageField(upload_to=cargarFotoProducto, null=True)
    activo = models.IntegerField(blank=True, null=True)  

    def __str__(self):
        return self.idProducto+", "+self.nombreProducto+", "+str(self.stock)\
               +", "+str(self.precio)+", "+self.foto.__str__()

class Persona(models.Model):
    rut    = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    edad   = models.IntegerField(blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)  
   
    def __str__(self):
        return self.rut+", "+ self.nombre+", "+str(self.edad)+", "+str(self.activo)

class Genero(models.Model):
    id_tipo  = models.AutoField(db_column='idTipo', primary_key=True)  
    genero     = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return str(self.genero)


def cargarFoto(instance, filename):
    return "fotos/foto_{0}_{1}".format(instance.rut, filename )

class Usuario(Persona):
    id_tipo        = models.ForeignKey('app.Genero', models.DO_NOTHING, db_column='idTipo')
    fecha_nacimiento = models.DateField(db_column='fechaNacimiento', blank=True, null=True)
    foto             = models.ImageField(upload_to=cargarFoto, null=True)
    
    def __str__(self):
        return self.rut+", "+ self.nombre+", "+str(self.edad)+", "\
               +str(self.id_tipo)+", "+str(self.fecha_nacimiento)+", "+str(self.activo)

User = get_user_model()

class Estado(models.Model):
    id_estado  = models.AutoField(db_column='idEstado', primary_key=True)  
    estado     = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return str(self.estado)

class Venta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fechaVenta=models.DateTimeField(auto_now_add=True)
    estado = models.ForeignKey(Estado,default=1,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'ventas'
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
        ordering = ["id"]

class DetalleVenta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta_id = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    cfechaDetalle=models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f'{self.cantidad} unidades de {self.producto_id.nombreProducto}'

    class Meta:
        db_table = 'detalleventas'
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalle Ventas'
        ordering = ["id"]
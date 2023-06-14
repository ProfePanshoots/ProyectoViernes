from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length=300)
    tipo = models.ForeignKey(TipoProducto,on_delete=models.DO_NOTHING)
    imagen = models.ImageField(upload_to="productos",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.nombre
    
CustomUser = get_user_model()

class Subscripciones(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    suscrito = models.BooleanField(default=False)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_termino = models.DateField(auto_now_add=True)
    # Otros campos relacionados con la suscripción

    def __str__(self):
        return f'{self.user.get_username}'
    

class Item_Carrito(models.Model):

    nombre_producto = models.CharField(max_length=40)
    precio_producto = models.IntegerField()
    imagen = models.ImageField(upload_to="items_carrito",null=True)
    cantidad = models.IntegerField(default=1)


    def __str___(self):
        return self.nombre_producto
    
    class Meta:
        db_table = "db_items_carrito"

    
    def calcular_subtotal(self):
        return self.precio_producto * self.cantidad
        
#pteguntar chat gtp como transformar la funcion en una linea
    def calcular_total_carrito():
        total = 0
        items_carrito = Item_Carrito.objects.all()
        for item in items_carrito:
            total += item.precio_producto * item.cantidad
        return total
       
    def sumar_cantidad(self):
        self.cantidad += 1
        self.save()
        
    
    def restar_cantidad(self):
        if self.cantidad > 1:
            self.cantidad -= 1
            self.save()

    @classmethod
    def vaciar_carrito(cls):
        cls.objects.all().delete()
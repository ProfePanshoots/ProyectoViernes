from django.contrib import admin
from .models import *

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','stock','tipo']
    list_editable = ['precio','stock']
    search_fields = ['stock','tipo']
    list_filter = ['tipo','stock']
    list_per_page = 10

class TipoProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    
class Item_Carrito_Admin(admin.ModelAdmin):
    list_display = ['nombre_producto']

class SubscripcionesAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Subscripciones,SubscripcionesAdmin)
admin.site.register(Item_Carrito,Item_Carrito_Admin)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(TipoProducto,TipoProductoAdmin)
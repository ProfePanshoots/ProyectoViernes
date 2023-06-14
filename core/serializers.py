# SE ENCARGA DE CONVERTIR LA DATA
from .models import *
from rest_framework import serializers

#Este archivo se encargara de convertir los datos a json o de json podra guardar, modificar, listar
# y eliminar datos

class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    tipo = TipoProductoSerializer(read_only=True)
    tipo_id = serializers.PrimaryKeyRelatedField(queryset = TipoProducto.objects.all(), source="tipo")
    nombre = serializers.CharField(required=True, min_length=3)

    def validate_nombre(self, value):
        existe = Producto.objects.filter(nombre=value).exists()

        if existe:
            raise serializers.ValidationError("Este producto ya existe")
        
        return value

    class Meta:
        model = Producto
        fields = '__all__'



from django.forms import ValidationError
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseServerError
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.contrib.auth.models import User
#rest_framework
from rest_framework import viewsets
from .serializers import *
import requests
from datetime import datetime

# Create your views here.

# SE ENCARGA DE MOSTRAR EN LA VISTA LOS DATOS

#toma los datos y guardarlos en caso de haber un json
class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    #queryset = Producto.objects.filter(tipo=1)
    serializer_class = ProductoSerializer


#Perfil

@login_required
@user_passes_test(lambda u: u.is_superuser)
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def perfil(request):
    user = request.user
    try:
        subscripciones = Subscripciones.objects.get(user=user)
        is_subscribed = subscripciones.suscrito
    except Subscripciones.DoesNotExist:
        is_subscribed = False
    return render(request,'core/profile.html', {'user': user, 'is_subscribed': is_subscribed}) 

def index(request):
    productos = Producto.objects.all()

    respuesta = requests.get('https://mindicador.cl/api')

    #transformamos a json
    monedas = respuesta.json()


    data = {
        'listadoProductos':productos,
        'monedas': monedas
    }

    return render(request,'core/index.html',data)

#SUSCRIPCIONES
@login_required
def suscribirse(request):
    if request.method == 'POST':
        form = SubscripcionForm(request.POST)
        if form.is_valid():
            try:
                suscripcion = form.save(commit=False)
                suscripcion.user = request.user
                suscripcion.save()
                messages.success(request, "Te has suscrito satisfactoriamente")
                return redirect('perfil')
            except Exception as e:
                messages.error(request, "El usuario ya se encuentra suscrito")
                return redirect('perfil')
    else:
        form = SubscripcionForm()
    
    return render(request, 'core/cruds/add-subscripcion.html', {'form': form})

@login_required
def desuscribirse(request):
    
    if request.method == 'POST':
        try:
            suscripcion = Subscripciones.objects.get(user=request.user)
            messages.success(request,"Te has desuscrito satisfactoriamente")
            suscripcion.delete()
            return redirect('perfil')  # Reemplaza 'ruta_de_exito' con la URL a la que deseas redirigir después de la desuscripción exitosa
        except Exception as e:
            messages.error(request,"El usuario se encuentra actualmente desuscrito")
    else:
        return render(request, 'core/cruds/desuscribirse.html')

    return redirect(to="perfil")
#END SUBSCRIPCIONES


@login_required
def shop(request):
    productos = Producto.objects.all()

    #REALIZAMOS LA SOLICITUD A LA API
    respuesta = requests.get('https://mindicador.cl/api')

    #Transformamos json
    monedas = respuesta.json()
    data = {
        'listadoProductos':productos,
        'monedas':monedas
    }

    if request.method == 'POST':
        carrito = Item_Carrito()
        carrito.nombre_producto = request.POST.get('nombre_producto')
        carrito.precio_producto = request.POST.get('precio_producto')
        carrito.imagen = request.POST.get('imagen_producto')
        messages.success(request, "Producto guardado en el carro satisfactoriamente")
        carrito.save()
        


    return render(request,'core/shop.html',data)

@login_required
def shopApi(request):
    #REALIZAMOS LA SOLICITUD A LA API
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    respuesta2 = requests.get('https://mindicador.cl/api')
    respuesta3 = requests.get('https://rickandmortyapi.com/api/character')
    respuesta4 = requests.get('https://digimon-api.vercel.app/api/digimon')
    # TRANSFORMAMOS EL JSON PARA LEERLO
    productos = respuesta.json()
    monedas = respuesta2.json()
    aux = respuesta3.json()
    personajes = aux['results']
    digimon = respuesta4.json()

    data = {
        'listadoProductos': productos,
        'monedas': monedas,
        'personajes': personajes,
        'digimon': digimon,
    }
    return render(request,'core/shopApi.html',data)

@login_required
def carrito(request):
    productos = Item_Carrito.objects.all()
    items_carrito = Item_Carrito.objects.all()
    total_carrito = Item_Carrito.calcular_total_carrito()

    

    #LOGICA CONVERSION PARA EL CARRO DE COMPRAS
    #API MONEDAS
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor'] # Llamamos al valor del dolar mediante la api
    data = {
        'listadoCarrito': productos,
        'items_carrito': items_carrito,
        'total_carrito': round(total_carrito/valor_usd,2), #Conversion a dolar
        
        #APIS

        
    }

    


    return render(request,'core/carrito.html',data)


def sumar_cantidad(request, producto_id):
    item = get_object_or_404(Item_Carrito, id=producto_id)

    if request.method == 'POST':
        item.sumar_cantidad()
        
        return redirect('carrito')

def restar_cantidad(request, producto_id):
    item = get_object_or_404(Item_Carrito, id=producto_id)
    
    if request.method == 'POST':
        precio_anterior = item.precio_producto

        try:
            if item.cantidad > 1:
                item.restar_cantidad()
            else:
                item.precio_producto = item.producto.precio  # Restaurar el precio inicial si la cantidad es 1

            if item.cantidad < 1:
                return redirect('carrito')

            item.save()
            return redirect('carrito')

        #hacemos una excepcion en el caso de que restemos menos de un producto
        except Exception as e:
            # Manejar la excepción aquí
            # Por ejemplo, mostrar un mensaje de error en la página
            messages.error(request,"Error al restar cantidad al carrito")
            return redirect(to="carrito")
    
def eliminar_item_carrito(request,producto_id):
    item_carrito = get_object_or_404(Item_Carrito, id = producto_id)
    item_carrito.delete()

    return redirect(to="carrito")

def vaciar_carrito(request):
    Item_Carrito.vaciar_carrito()
    messages.success(request,'Se ha eliminado el carrito de compras')
    return redirect('carrito')

def contacto(request):
    return render(request,'core/contact.html')


#CRUD
#AGREGAR
@permission_required('core.add_producto')
def addproducto(request):
    data ={
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES) #Recibe el contenido del formulario
        if formulario.is_valid():
            formulario.save()#insert
            data['msj'] = "Producto Almacenado Correctamente! "
        return redirect(to="shop")

    return render(request, 'core/cruds/add-producto.html',data)

#Listar
@permission_required('core.view_producto')
 
def listarproductos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(productos,5)
        productos = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'productos': productos,
        'paginator': paginator
    }
    return render(request,'core/cruds/listar-productos.html',data)


#UPDATE
@permission_required('core.change_producto')
def modificarproducto(request,id):
    producto = Producto.objects.get(id=id) 
    data ={
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST,instance=producto, files=request.FILES) #Recibe el contenido del formulario
        if formulario.is_valid():
            formulario.save() #insert
            messages.success(request, "Producto modificado correctamente")
            return redirect(to="listarproductos")
        data['form'] = formulario

    return render(request, 'core/cruds/modificar-producto.html',data)

#DELETE
@permission_required('core/delete_producto')
def eliminarproducto(request,id):
    producto = Producto.objects.get(id=id)
    messages.success(request, "Producto eliminado correctamente") 
    producto.delete()

    return redirect(to="listarproductos")

#Registrar usuarios
def registrousuarios(request):
    data = {
        'form':CustomUserCreationForm
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid:
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            login(request,user)
            messages.success(request, "Te has registrado correctamente")
            #redirigir el home
            return redirect(to="index")
        data["form"] = formulario
    return render(request,'registration/registro.html',data)
from .views import *
from django.urls import path,include
from django.contrib.auth import views as auth_views
#rest_framework
from rest_framework import routers

#RUTA DEL API

router = routers.DefaultRouter()
#registra la url
router.register('productos', ProductoViewset)

urlpatterns = [ #Rutas de urls
    #API: localhost:800/api/producto
    path('api/',include(router.urls)),
    
    #RUTAS
    path('', index,name="index"),
    path('perfil/',perfil,name="perfil"),
    path('contacto/',contacto,name="contacto"),
    path('shop/',shop,name="shop"),
    path('shopApi/',shopApi,name="shopApi"),
    #Carro de compras
    path('carrito/',carrito,name="carrito"),
    path('sumar_cantidad/<int:producto_id>/', sumar_cantidad, name='sumar_cantidad'),
    path('restar_cantidad/<int:producto_id>/', restar_cantidad, name='restar_cantidad'),
    path('eliminar_item_carrito/<int:producto_id>/',eliminar_item_carrito,name="eliminar_item_carrito"),
    path('vaciar_carrito',vaciar_carrito,name="vaciar_carrito"),
    #Subscripcion
    path('suscribirse/', suscribirse, name='suscribirse'),
    path('desuscribirse/', desuscribirse, name='desuscribirse'),
    #CRUD
    path('addproducto/',addproducto, name="addproducto"),
    path('listarproductos/',listarproductos,name="listarproductos"),
    path('modificarproducto/<int:id>/',modificarproducto, name="modificarproducto"),
    path('eliminarproducto/<int:id>/',eliminarproducto,name="eliminarproducto"),
    path('registrousuarios/',registrousuarios,name="registrousuarios"),
    #urls recuperar contraseña, recordar preguntar profe
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
     
]

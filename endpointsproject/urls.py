"""
URL configuration for endpointsproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views.connekta_siesa.jsons.inventario import inventario
from views.contaPymes.art import getart, postart
from views.contaPymes.authentication import authentication
from views.connekta_siesa.jsons.requisicion1 import requesicion1
from views.connekta_siesa.jsons.requisicion2 import requesicion2
from views.connekta_siesa.jsons.requisicion3 import requesicion3
from views.connekta_siesa.peticiones.conectores_importar import conectores_importar
from views.contaPymes.clientes import getclientes
from views.contaPymes.clt import getclt, postclt
from views.contaPymes.dpk import getdpk, getepk, postdpk
from views.contaPymes.epk import getepk, postepk
from views.connekta_siesa.jsons.generar_recibo import generar_recibo
from views.contaPymes.inventoryOperation import getbyordernumber
from views.connekta_siesa.peticiones.validar_entrada_compra import validar_entrada_compra
from views.contaPymes.operaciones import getoperaciones
from views.contaPymes.pedido import createpedido
from views.contaPymes.productos import getproductos

urlpatterns = [
    path('admin/', admin.site.urls),

    # Endpoints conexion y obtencion de informacion de ContaPymes
    path('authentication/', authentication),
    path('getByOrderNumber/', getbyordernumber),
    path('getoperaciones/', getoperaciones),
    path('getproductos/', getproductos),
    path('getclientes/', getclientes),

    # Endpoints para el WMS
    path('dpk/get/', getdpk),
    path('dpk/post/', postdpk),
    path('clt/get/', getclt),
    path('clt/post/', postclt),
    path('epk/get/', getepk),
    path('epk/post/', postepk),
    path('art/get/', getart),
    path('art/post/', postart),
    path('createpedido/', createpedido),
    
    # Endpoints SIESA
    path('validar_entrada_compra/', validar_entrada_compra),
    path('generar_recibo/', generar_recibo),
    path('conectores_importar/', conectores_importar),

    path('requisicion1json/', requesicion1),
    path('requisicion2json/', requesicion2),
    path('requisicion3json/', requesicion3),
    path('inventariojson/', inventario),

]
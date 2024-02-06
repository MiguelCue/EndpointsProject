from django.http import JsonResponse
from dotenv import load_dotenv
import requests
import os
from json import loads
from views.contaPymes.epk import getepk
from datetime import datetime
from django.utils import timezone 

from views.contaPymes.inventoryOperation import getbyordernumber

config = load_dotenv()

def postdpk(request):
    url = "https://api.copernicowms.com/wms/dpk"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": os.getenv("APIKEY")
    }

    invope = getbyordernumber(request)
    epk = getepk(request)

    epkdata = loads(epk.content).get('epk', [])[0]
    invopedata = loads(invope.content).get('datos', {})
    listaproductos = invopedata.get('listaproductos', [])

    doctoerp = epkdata.get('doctoerp', None)
    picking = epkdata.get('picking', None)
    tipodocto = epkdata.get('tipodocto', None)
    numpedido = epkdata.get('numpedido', None)
    item = epkdata.get('item', None)
    
    fecha_actual = timezone.now()
    
    print(fecha_actual)
    dpk = []

    for producto in listaproductos:
        irecurso = producto.get('irecurso', None) # Código producto
        #sobserv = producto.get('sobserv', None) # Descripcion
        qrecurso = producto.get('qrecurso', None) # Cantidad
        mprecio = producto.get('mprecio', None) # Precio Unitario
        iinventario = producto.get('iinventario', None) # Código de la bodega 

        payload = {
            "referencia": irecurso,
            "refpadre": irecurso,
            "descripcion": "",#Falta corregir
            "qtypedido": qrecurso,
            "qtyreservado": qrecurso,
            "productoean": irecurso,
            "picking": picking,
            "lineaidpicking": None,
            "costo": mprecio,
            "bodega": iinventario,
            "tipodocto": tipodocto,
            "doctoerp": doctoerp,
            "qtyenpicking": 0,
            "estadodetransferencia": 0,
            "fecharegistro": fecha_actual,
            "ubicacion_plan": None,
            "fechatransferencia": None,
            "clasifart": None,
            "serial": None,
            "item": item,
            "idco": None,
            "qtyremisionado": None,
            "qtyfacturado": None,
            "preciounitario": mprecio,
            "notasitem": "",
            "descripcionco": None,
            "factor": 0,
            "numpedido": numpedido,
            "pedproveedor": "NA",
            "loteproveedor": "NA",
            "field_qtypedidabase": None,
            "lineaidpickingint": None,
            "f_ultima_actualizacion": fecha_actual
        }

        
        
        dpk.append(payload)

        
        

    return JsonResponse({'dpk': dpk})

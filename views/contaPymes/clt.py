from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os
from django.utils import timezone

config = load_dotenv()
APIKEY = 'vPRLHH1Bx)gg51-iiza5c#dJ}Lp&e1edjBgbQjX!VUBmMRcNW=9JTQ!3taFmymu%NZy;ki*D]jM630%dA1'
def getclt(request):
    item = request.GET.get('item', None)
    
    url = 'https://api.copernicowms.com/wms/clt'

    if item:
        url += f"?item={item}"

    headers = {
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        clt = loads(response.content)
        if len(clt) >= 1:
            return JsonResponse({'clt': clt[0]})
        else:
            return JsonResponse({'clt': []})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text})
    

def postclt(request):
    url = "https://api.copernicowms.com/wms/clt"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    clt = request.GET.get('clt', {})
    
    item = clt.get('item', None)
    nombre = clt.get('nombre', None)
    email = clt.get('email', None)
    contacto = clt.get('contacto', None)
    direccion = clt.get('direccion', None)
    pais = clt.get('pais', None)
    departamento = clt.get('departamento', None)
    ciudad = clt.get('ciudad', None)
    ipais = clt.get('ipais', None)
    idepartamento = clt.get('idepartamento', None)
    iciudad = clt.get('iciudad', None)
    notas = clt.get('sobservaciones', None)
    

    payload = {
        "nit": item,
        "nombrecliente": nombre,
        "direccion": direccion,
        "isactivoproveedor": None,
        "condicionescompra": None,
        "codigopais": None,
        "monedadefacturacion": None,
        "item": item,
        "activocliente": 1,
        "ciudaddestino": ciudad,
        "dptodestino": departamento,
        "paisdestino": pais,
        "codciudaddestino": iciudad,
        "coddptodestino": idepartamento,
        "codpaisdestino": ipais,
        "fecharegistro": None,
        "telefono": contacto,
        "cuidad": ciudad,
        "cuidaddespacho": None,
        "notas": notas,
        "contacto": contacto,
        "email": email,
        "paisdespacho": "Colombia",
        "departamentodespacho": None,
        "sucursaldespacho": None,
        "idsucursal": None,
        "isactivocliente": 1,
        "isactivoproveed": 1,
        "estadotransferencia": 0,
        "vendedor": None,
        "zip_code": None,
        "licencia": None,
        "compania": None
    }
    #return JsonResponse({'clt': payload})
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        
        return JsonResponse({'clt': payload})
    else:
        return JsonResponse({'Error': response.status_code, 'text': "Client creation error", 'payload': payload})

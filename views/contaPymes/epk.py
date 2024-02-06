from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os

from views.contaPymes.inventoryOperation import getbyordernumber

config = load_dotenv()

def getepk(request):
    doctoerp = request.GET.get('doctoerp', None)
    
    url = 'https://api.copernicowms.com/wms/epk'

    if doctoerp:
        url += f"?doctoerp={doctoerp}"

    headers = {
        "Accept": "application/json",
        "Authorization": os.getenv("APIKEY")
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse({'epk': response.json()})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text})


@csrf_exempt
def postepk(_, snumsop):
    url = 'https://api.copernicowms.com/wms/epk'

    invope = getbyordernumber(_, snumsop)
    invopedata = loads(invope.content).get('datos', {})
    
    header = invopedata.get("encabezado", {})
    snumsop = header.get("snumsop", None)
    inumoper = header.get("inumoper", None)
    iusuario = header.get("iusuario", None)

    principaldata = invopedata.get("datosprincipales", {})
    init  = principaldata.get("init", None)
    sobserv = principaldata.get("sobserv", None)

    payload = {
        "tipodocto": "FLT",
        "doctoerp": snumsop,
        "numpedido": inumoper,
        "fechaplaneacion": None,
        "f_pedido": None,
        "item": init,
        "nombrecliente": iusuario,
        "contacto": None,
        "email": None,
        "notas": sobserv,
        "ciudad_despacho": None,
        "pais_despacho": None,
        "departamento_despacho": None,
        "sucursal_despacho": None,
        "direccion_despacho": None,
        "idsucursal": None,
        "ciudad": None,
        "pedidorelacionado": snumsop,
        "cargue": "",
        "nit": init,
        "estadopicking": 0,
        "fecharegistro": None,
        "fpedido": None,
        "fechtrans": None,
        "transportadora": None,
        "centrooperacion": None,
        "estadoerp": None,
        "picking_batch": None,
        "field_condicionpago": None,
        "field_documentoreferencia": None,
        "bodega": None,
        "vendedor2": None,
        "numguia": None,
        "f_ultima_actualizacion": None,
        "bodegaerp": None
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": os.getenv("APIKEY")
    }  

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return JsonResponse({'success':response.json().get('success', None),
                             'payload': payload})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text, 'data': payload})

    

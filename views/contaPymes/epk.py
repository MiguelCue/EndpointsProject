from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os

from views.contaPymes.clientes import getclientes
from views.contaPymes.clt import getclt, postclt
from views.contaPymes.inventoryOperation import getbyordernumber

config = load_dotenv()

APIKEY = 'vPRLHH1Bx)gg51-iiza5c#dJ}Lp&e1edjBgbQjX!VUBmMRcNW=9JTQ!3taFmymu%NZy;ki*D]jM630%dA1'

def getepk(request):
    doctoerp = request.GET.get('doctoerp', None)
    
    url = 'https://api.copernicowms.com/wms/epk'

    if doctoerp:
        url += f"?doctoerp={doctoerp}"

    headers = {
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        epk = loads(response.content)
        if len(epk) >= 1:
            return JsonResponse({'epk': epk[0]})
        else:
            return JsonResponse({'epk': []})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text})


@csrf_exempt
def postepk(request):
    url = 'https://api.copernicowms.com/wms/epk'
    new_request = type('Request', (), {})()

    pedidojson = getbyordernumber(request)
    pedido = loads(pedidojson.content).get('pedido', {})
    
    encabezado = pedido.get("encabezado", {})
    snumsop = encabezado.get("snumsop", None)
    inumoper = encabezado.get("inumoper", None)
    fprocesam = encabezado.get("fprocesam", None)
    iprocess = encabezado.get("iprocess", None)

    principaldata = pedido.get("datosprincipales", {})
    init = principaldata.get("init", None)
    iinventario = principaldata.get("iinventario", None)
    sobserv = principaldata.get("sobserv", None)
    isucursalcliente = principaldata.get("isucursalcliente", None)

    setattr(new_request, 'GET', {'item': init})
    cltjson = getclt(new_request)
    clt = loads(cltjson.content).get('clt', {})
    
    if clt:
        nombre = clt.get('nombrecliente', None)
        direccion = clt.get('direccion', None)
        contacto = clt.get('contacto', None)
        email = clt.get('email', None)
        ciudad = clt.get('ciudaddestino', None)
        departamento = clt.get('dptodestino', None)
        pais = clt.get('paisdestino', None)
        
    else:
        setattr(new_request, 'GET', {'init': init})
        clientejson = getclientes(new_request)
        cliente = loads(clientejson.content).get('cliente', {})
        
        infobasica = cliente.get('infobasica', {})
        ntercero = infobasica.get('ntercero', None)
        napellido = infobasica.get('napellido', None)
        nombre = ntercero + " " + napellido
        email = infobasica.get('semail', None)
        contacto = infobasica.get('ttelefono', None)
        direccion = infobasica.get('tdireccion', None)
        pais = infobasica.get('npais', None)
        departamento = infobasica.get('ndep', None)
        ciudad = infobasica.get('nmun', None)
        ipais = infobasica.get('ipais', None)
        idepartamento = infobasica.get('idep', None)
        iciudad = infobasica.get('imun', None)
        sobservaciones = infobasica.get('sobservaciones', None)

        setattr(new_request, 'GET', {'clt': {
                                        'item': init,
                                        'nombre': nombre,
                                        'email': email,
                                        'contacto': contacto,
                                        'direccion': direccion,
                                        'pais': pais,
                                        'departamento': departamento,
                                        'ciudad': ciudad,
                                        'ipais': ipais,
                                        'idepartamento': idepartamento,
                                        'iciudad': iciudad,
                                        'sobservaciones': sobservaciones
                                    }})
        
        responseclt = postclt(new_request)
        clt = loads(responseclt.content).get('clt', {})

    payload = {
        "tipodocto": "FLT",
        "doctoerp": snumsop,
        "numpedido": inumoper,
        "fechaplaneacion": None,
        "f_pedido": fprocesam,
        "item": init,
        "nombrecliente": nombre,
        "contacto": contacto,
        "email": email,
        "notas": sobserv,
        "ciudad_despacho": ciudad,
        "pais_despacho": pais,
        "departamento_despacho": departamento,
        "sucursal_despacho": isucursalcliente,
        "direccion_despacho": direccion,
        "idsucursal": None,
        "ciudad": ciudad,
        "pedidorelacionado": snumsop,
        "cargue": "",
        "nit": init,
        "estadopicking": 0,
        "fecharegistro": fprocesam,
        "fpedido": fprocesam,
        "fechtrans": None,
        "transportadora": None,
        "centrooperacion": None,
        "estadoerp": iprocess,
        "picking_batch": None,
        "field_condicionpago": None,
        "field_documentoreferencia": None,
        "bodega": iinventario,
        "vendedor2": None,
        "numguia": None,
        "f_ultima_actualizacion": None,
        "bodegaerp": iinventario
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": APIKEY
    }  
    #return JsonResponse({'epk': payload, 'clt': clt})
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return JsonResponse({'epk': payload, 'clt': clt})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text, 'payload': payload})
    
 
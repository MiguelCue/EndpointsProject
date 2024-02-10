from django.http import JsonResponse
from dotenv import load_dotenv
import requests
import os
from json import loads
from views.contaPymes.art import getart, postart
from views.contaPymes.epk import getepk
from django.utils import timezone 

from views.contaPymes.inventoryOperation import getbyordernumber
from views.contaPymes.productos import getproductos

config = load_dotenv()

APIKEY = 'vPRLHH1Bx)gg51-iiza5c#dJ}Lp&e1edjBgbQjX!VUBmMRcNW=9JTQ!3taFmymu%NZy;ki*D]jM630%dA1'

def getdpk(request):
    productoean = request.GET.get('productoean', None)
    url = 'https://api.copernicowms.com/wms/dpk'

    if productoean:
        url += f"?productoean={productoean}"

    headers = {
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse({'dpk': response.json()})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text})


def postdpk(request):
    url = "https://api.copernicowms.com/wms/dpk"
    new_request = type('Request', (), {})() # Crear un objeto request vacío

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    doctoerp = request.GET.get('doctoerp', None)
    epkjson = getepk(request)
    epk = loads(epkjson.content).get('epk', {})

    if not epk:
        return JsonResponse({'Error': f'There is no a EPK identified with "doctoerp": {doctoerp}'}) 
    
    invope = getbyordernumber(request)
    invopedata = loads(invope.content).get('pedido', {})
    listaproductos = invopedata.get('listaproductos', [])
    picking = epk.get('picking', None)
    tipodocto = epk.get('tipodocto', None)
    numpedido = epk.get('numpedido', None)
    item = epk.get('item', None)
    fecharegistro = epk.get('fecharegistro', None)
    fecha_actual = timezone.now().isoformat()
    
    dpk = []

    i = 4038392
    for producto in listaproductos:
        irecurso = producto.get('irecurso', None) # Código producto
        qrecurso = producto.get('qrecurso', None) # Cantidad
        iinventario = producto.get('iinventario', None) # Código de la bodega 
        mvrtotal = producto.get('mvrtotal', None)
        costo = producto.get('mprecio', None)

        setattr(new_request, 'GET', {'irecurso': irecurso})
        productojson = getproductos(new_request)
        producto = loads(productojson.content).get('producto', )[0]
        
        clase1 = producto.get('clase1', "")
        clase2 = producto.get('clase2', "")
        tipo1 = producto.get('tipo1', "")
        tipo2 = producto.get('tipo2', "")
        
        descripcion = producto.get('nrecurso', None)
        observacion = producto.get('sobservaciones', None)
        # nunidad = producto.get('nunidad', None)
        # qfactor = producto.get('qfactor', None)

        # setattr(new_request, 'GET', {'productoean': irecurso})
        # artjson = getart(new_request)
        # art = loads(artjson.content).get('art', [])

        # if art:
        #     descripcion = art[0].get('descripcion', None)
        #     costo = art[0].get('costo', None)
        #     observacion = art[0].get('observacion', None)
        # else:
        #     descripcion = producto.get('nrecurso', None)
        #     observacion = producto.get('sobservaciones', None)
        #     nunidad = producto.get('nunidad', None)
        #     qfactor = producto.get('qfactor', None)
            
        #     setattr(new_request, 'GET', {'art' : {
        #                                     'irecurso': irecurso,
        #                                     'descripcion': descripcion,
        #                                     'costo': costo,
        #                                     'nunidad': nunidad,
        #                                     'qfactor': qfactor,
        #                                     'iinventario': iinventario,
        #                                     'sobservaciones': observacion,
        #                                     }})
        #     responseart = postart(new_request)
        #     art = loads(responseart.content).get('art', {})
            

        payload = {
            "referencia": irecurso,
            "refpadre": irecurso,
            "descripcion": descripcion,
            "qtypedido": qrecurso,
            "qtyreservado": qrecurso,
            "productoean": irecurso,
            "picking": picking,
            "lineaidpicking": i,
            "costo": mvrtotal,
            "bodega": iinventario,
            "tipodocto": tipodocto,
            "doctoerp": doctoerp,
            "qtyenpicking": 0,
            "estadodetransferencia": 0,
            "fecharegistro": fecharegistro,
            "ubicacion_plan": None,
            "fechatransferencia": None,
            "clasifart": None,
            "serial": None,
            "item": item,
            "idco": None,
            "qtyremisionado": None,
            "qtyfacturado": None,
            "preciounitario": costo,
            "notasitem": observacion,
            "descripcionco": clase1 + " " + clase2 + " " + tipo1 + " " + tipo2,
            "factor": 0,
            "numpedido": numpedido,
            "pedproveedor": "NA",
            "loteproveedor": "NA",
            "field_qtypedidabase": None,    
            "f_ultima_actualizacion": fecha_actual
        }

        i += 1
        print(payload)
        dpk.append({'dpk': payload})
        
        response = requests.post(url, json=payload, headers=headers)
        # return JsonResponse({'status': response.status_code,
        #                      'data': response.json(),
        #                      'dpk': payload}) 

    if dpk:
        return JsonResponse({'data': dpk})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text, 'dpk': dpk})

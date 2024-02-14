from django.utils import timezone 
from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os

from views.contaPymes.inventoryOperation import getbyordernumber
from views.contaPymes.productos import getproductos
from views.contaPymes.art import getart, postart
from views.contaPymes.epk import getepk

config = load_dotenv()
APIKEY = os.getenv('APIKEY')

def getdpk(request):
    doctoerp = request.GET.get('doctoerp', None)
    url = 'https://api.copernicowms.com/wms/dpk'

    if doctoerp:
        url += f"?doctoerp={doctoerp}"

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

    dpkjson = getdpk(request)
    dpk = loads(dpkjson.content).get('dpk', {})
    if dpk:
        print(f'Error: The DPK {doctoerp} exist in WMS')
        return JsonResponse({'Error': f'There is a DPK identified with: {doctoerp}',
                             'dpk': dpk}, status=500) 

    epkjson = getepk(request)
    epk = loads(epkjson.content).get('epk', {})

    if not epk:
        print(f'Error: The Epk {doctoerp} does not exist in WMS')
        return JsonResponse({'Error': f'There is no a EPK identified with: {doctoerp}'}) 
    
    pedidojson = getbyordernumber(request)
    pedido = loads(pedidojson.content).get('pedido', {})

    if not pedido:
        print(f'Error: The order {doctoerp} does not exist in ContaPymes')
        return JsonResponse({'Error': f'The order {doctoerp} does not exist in ContaPymes'}, status=500)
    
    listaproductos = pedido.get('listaproductos', [])
    picking = epk.get('picking', None)
    tipodocto = epk.get('tipodocto', None)
    numpedido = epk.get('numpedido', None)
    item = epk.get('item', None)
    fecharegistro = epk.get('fecharegistro', None)
    fecha_actual = timezone.now().isoformat()
    
    #pedidoanterior = _getpedidoanterior(doctoerp)
    #return JsonResponse({'anterior': pedidoanterior})
    
    dpk = []

    i = 4039018
    for producto in listaproductos:
        irecurso = producto.get('irecurso', None) # Código producto
        qrecurso = producto.get('qrecurso', None) # Cantidad
        iinventario = producto.get('iinventario', None) # Código de la bodega 
        mvrtotal = producto.get('mvrtotal', None)
        costo = producto.get('mprecio', None)

        setattr(new_request, 'GET', {'productoean': irecurso})
        artjson = getart(new_request)
        art = loads(artjson.content).get('art', [])

        if art:
            descripcion = art[0].get('descripcion', None)
            costo = art[0].get('costo', None)
            observacion = art[0].get('observacion', None)
            descripcionco = art[0].get('descripcionco', None)
            
        else:
            setattr(new_request, 'GET', {'irecurso': irecurso})
            productojson = getproductos(new_request)
            producto = loads(productojson.content).get('producto', )[0]

            if not producto:
                print(f'Error: The item {irecurso} does not exist in ContaPymes')
                return JsonResponse({'Error': f'The order {doctoerp} does not exist in ContaPymes'}, status=500)

            clase1 = producto.get('clase1', "")
            clase2 = producto.get('clase2', "")
            tipo1 = producto.get('tipo1', "")
            tipo2 = producto.get('tipo2', "")
            descripcion = producto.get('nrecurso', None)
            observacion = producto.get('sobservaciones', None)
            descripcion = producto.get('nrecurso', None)
            nunidad = producto.get('nunidad', None)
            qfactor = producto.get('qfactor', None)
            descripcionco =  clase1 + " " + clase2 + " " + tipo1 + " " + tipo2
            
            setattr(new_request, 'GET', {'art' : {
                                            'irecurso': irecurso,
                                            'descripcion': descripcion,
                                            'costo': costo,
                                            'nunidad': nunidad,
                                            'qfactor': qfactor,
                                            'iinventario': iinventario,
                                            'sobservaciones': observacion,
                                            }})
            responseart = postart(new_request)
            art = loads(responseart.content).get('art', {})
        
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
            "descripcionco":descripcionco,
            "factor": 0,
            "numpedido": numpedido,
            "pedproveedor": "NA",
            "loteproveedor": "NA",
            "field_qtypedidabase": None,    
            "f_ultima_actualizacion": fecha_actual
        }

        i += 1
        print(payload)
        dpk.append({'dpk': payload,
                    'art': art})
        
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            return JsonResponse({'Error': 'DPK creation failed',
                                 'dpk': payload,
                                 'art': art})
        # return JsonResponse({'status': response.status_code,
        #                      'data': response.json(),
        #                      'dpk': payload}) 
    #return JsonResponse({'data': dpk})
    if dpk:
        return JsonResponse({'data': dpk})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text, 'dpk': dpk})
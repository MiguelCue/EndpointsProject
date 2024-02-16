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
APIKEY = 'vPRLHH1Bx)gg51-iiza5c#dJ}Lp&e1edjBgbQjX!VUBmMRcNW=9JTQ!3taFmymu%NZy;ki*D]jM630%dA1'

"""
Obtiene la información del DPK del sistema WMS.

Parámetros:
    request: Objeto HttpRequest que contiene el doctoerp de la solicitud.

Retorna:
    JsonResponse: Respuesta JSON que contiene la información del DPK si se obtiene con éxito, 
                    o un mensaje de error si la solicitud no es exitosa.
"""
def getdpk(request):
    doctoerp = request.GET.get('doctoerp', None)
    url = 'https://api.copernicowms.com/wms/dpk'

    # Si se proporciona el código de documento de ERP, agregarlo a la URL
    if doctoerp:
        url += f"?doctoerp={doctoerp}"
    else:
        # Devolver un mensaje de error si no se proporciona un código de doctoerp
        return JsonResponse({'Error': 'No doctoerp code was provided for filtering'}, status=403)
    
    # Encabezados para la solicitud HTTP
    headers = {
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    # Realizar la solicitud GET para obtener información del DPK
    response = requests.get(url, headers=headers)
    # Verificar el estado de la respuesta
    if response.status_code == 200:
        return JsonResponse({'dpk': response.json()})
    else:
        # Devolver un mensaje de error con el código de estado y el texto de la respuesta
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
        return JsonResponse({'Error': f'There is no a EPK identified with: {doctoerp}'}, status=500) 
    
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
    
    dpk = []

    i = 4039027
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
            producto = loads(productojson.content).get('producto', )

            if not producto:
                return JsonResponse({'Error': f'The item {irecurso} does not exist in ContaPymes'}, status=500)
            
            producto = producto[0]
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
    

"""
Crea un DPK en el sistema WMS.

Parámetros:
    request: Objeto HttpRequest que contiene la información de la solicitud.

Retorna:
    JsonResponse: Respuesta JSON que indica si el DPK se creó con éxito o no.
"""
def postdpkV2(request):
    url = "https://api.copernicowms.com/wms/dpk"
    new_request = type('Request', (), {})() # Crear un objeto request vacío
    
    # Encabezados para la solicitud HTTP
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": APIKEY
    }
    
    # Obtener los parámetros de la solicitud
    epk = request.GET.get('epk', None)
    pedido = request.GET.get('pedido', None)
    picking = request.GET.get('picking', None)

    # Obtener la lista de productos del pedido
    listaproductos = pedido.get('listaproductos', [])

    # Obtener datos específicos del EPK
    tipodocto = epk.get('tipodocto', None)
    doctoerp = epk.get('doctoerp', None)
    numpedido = epk.get('numpedido', None)
    item = epk.get('item', None)
    fecharegistro = epk.get('fecharegistro', None)
    fecha_actual = timezone.now().isoformat()

    i = 4039054 # ID inicial para la línea de picking
    for producto in listaproductos:
        irecurso = producto.get('irecurso', None) # Código producto
        qrecurso = producto.get('qrecurso', None) # Cantidad
        iinventario = producto.get('iinventario', None) # Código de la bodega 
        mvrtotal = producto.get('mvrtotal', None) # Total del movimiento
        costo = producto.get('mprecio', None) # Costo del producto

        # setattr(new_request, 'GET', {'productoean': irecurso})
        # artjson = getart(new_request)
        # art = loads(artjson.content).get('art', [])
        
        # if art:
        #     descripcion = art[0].get('descripcion', None)
        #     costo = art[0].get('costo', None)
        #     observacion = art[0].get('observacion', None)
        #     descripcionco = art[0].get('descripcionco', None)
        # else:

        # Realizar una solicitud GET para obtener información del producto
        setattr(new_request, 'GET', {'irecurso': irecurso})
        productojson = getproductos(new_request)
        producto = loads(productojson.content).get('producto', [])
        
        # Verificar si se encontró información del producto
        if not producto:
            return JsonResponse({'Error': f'The item {irecurso} does not exist in ContaPymes'}, status=500)
        else:
            # Extraer información relevante del producto
            producto = producto[0]
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
            
            # Realizar una solicitud POST para crear el producto en el sistema WMS
            # setattr(new_request, 'GET', {'art' : {
            #                                 'irecurso': irecurso,
            #                                 'descripcion': descripcion,
            #                                 'costo': costo,
            #                                 'nunidad': nunidad,
            #                                 'qfactor': qfactor,
            #                                 'iinventario': iinventario,
            #                                 'sobservaciones': observacion,
            #                                 }})
            # responseart = postart(new_request)
        
        # if responseart.status_code != 200:
        #     print(f'art {irecurso} creation failed')
        #     return JsonResponse({'Error': f'art {irecurso} creation failed'}, status=responseart.status_code)
        
            # Construir el payload para crear el DPK
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

            i += 1 # Incrementar el ID de la línea de picking
            
            # Realizar una solicitud POST para crear el DPK 
            response = requests.post(url, json=payload, headers=headers)

            # Verificar si la creación del DPK fue exitosa
            if response.status_code != 200:
                # Si la creación falla, devolver un mensaje de error
                return JsonResponse({'Error': 'DPK creation failed',
                                    'Text': response.text,
                                    'dpk': payload}, status=response.status_code)

    # Si se crearon todas las líneas de picking con éxito, devolver un mensaje de éxito            
    return JsonResponse({'Success': f'DPK {doctoerp} created'}, status=200)

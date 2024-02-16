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

"""
Obtiene la información del EPK del sistema WMS.

Parámetros:
    request: Objeto HttpRequest que contiene el doctoerp de la solicitud.

Retorna:
    JsonResponse: Respuesta JSON que contiene la información del EPK si se obtiene con éxito, 
                 o un mensaje de error si la solicitud no es exitosa.
"""
def getepk(request):
    doctoerp = request.GET.get('doctoerp', None)
    url = 'https://api.copernicowms.com/wms/epk'

    # Si se proporciona el número de documento de ERP, agregarlo a la URL
    if doctoerp:
        url += f"?doctoerp={doctoerp}"
    else: 
        return JsonResponse({'Error': 'No doctoerp code was provided for filtering'}, status=403)
    
    # Encabezados para la solicitud HTTP
    headers = {
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    # Realizar la solicitud GET para obtener información del EPK
    response = requests.get(url, headers=headers)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        epk = loads(response.content)
        # Verificar si se obtuvo al menos un EPK
        if len(epk) >= 1:
            # Devolver el primer EPK encontrado en formato JSON
            return JsonResponse({'epk': epk[0]})
        else:
            # Devolver una lista vacía si no se encontró ningún EPK
            return JsonResponse({'epk': []})
    else:
        # Devolver un mensaje de error con el código de estado y el texto de la respuesta
        return JsonResponse({'Error': response.status_code, 'text': response.text})

@csrf_exempt
def postepk(request):
    url = 'https://api.copernicowms.com/wms/epk'
    new_request = type('Request', (), {})()
    doctoerp = request.GET.get('doctoerp', None)

    epkjson = getepk(request)
    epk = loads(epkjson.content).get('epk', {})

    if epk:
        print(f'Error: The Epk {doctoerp} already exist in WMS')
        return JsonResponse({'Error': f'There is a EPK identified with: {doctoerp}'},  status=500) 
    
    pedidojson = getbyordernumber(request)
    pedido = loads(pedidojson.content).get('pedido', {})

    if not pedido:
        print(f'Error: The order {doctoerp} does not exist in ContaPymes')
        return JsonResponse({'Error': f'The order {doctoerp} does not exist in ContaPymes'}, status=500)
    
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
        "numpedido": snumsop,
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
        "field_documentoreferencia": inumoper,
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
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return JsonResponse({'epk': payload, 'clt': clt})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text, 'payload': payload})
    

"""
Crea un EPK en el sistema WMS.

Parámetros:
    request: Objeto HttpRequest que contiene el doctoerp de la solicitud.

Retorna:
    JsonResponse: Respuesta JSON que indica si el EPK se creó con éxito o no.
"""
def postepkV2(request):
    url = 'https://api.copernicowms.com/wms/epk'
    new_request = type('Request', (), {})()
    
    pedido = request.GET.get('pedido', {})

    # Extraxion de información del encabezado del pedido
    encabezado = pedido.get("encabezado", {})
    snumsop = encabezado.get("snumsop", None)
    inumoper = encabezado.get("inumoper", None)
    fprocesam = encabezado.get("fprocesam", None)
    iprocess = encabezado.get("iprocess", None)

    # Extraxion de información principal del pedido
    principaldata = pedido.get("datosprincipales", {})
    iinventario = principaldata.get("iinventario", None)
    init = principaldata.get("init", None)
    sobserv = principaldata.get("sobserv", None)
    isucursalcliente = principaldata.get("isucursalcliente", None)

    # Configurar la solicitud con la identificacion del cliente 
    setattr(new_request, 'GET', {'item': init})
    
    # Verificar si existe el cliente en el WMS
    cltjson = getclt(new_request)
    clt = loads(cltjson.content).get('clt', {})  
    if clt:
        # Obtener la informacion del cliente desde WMS
        nombre = clt.get('nombrecliente', None)
        direccion = clt.get('direccion', None)
        contacto = clt.get('contacto', None)
        email = clt.get('email', None)
        ciudad = clt.get('ciudaddestino', None)
        departamento = clt.get('dptodestino', None)
        pais = clt.get('paisdestino', None)
    else:
        setattr(new_request, 'GET', {'init': init})
        # Obtener la informacion del cliente desde ContaPyme
        clientejson = getclientes(new_request)
        cliente = loads(clientejson.content).get('cliente', {})
        
        # Extracion de la información básica del cliente
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

        # Configurar la solicitud con la información para crear el cliente en el WMS
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
        
        # Creacion del cliente en el WMS
        responseclt = postclt(new_request)
        if responseclt.status_code != 200:
            print(f'CLT {init} could not be created in WMS')
            return JsonResponse({'Error': f'CLT {init} could not be created in WMS'}, status=responseclt.status_code)

    # Json para la creación del EPK
    payload = {
        "tipodocto": "FLT",
        "doctoerp": snumsop,
        "picking": None,
        "numpedido": snumsop,
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
        "field_documentoreferencia": inumoper,
        "bodega": iinventario,
        "vendedor2": None,
        "numguia": None,
        "f_ultima_actualizacion": None,
        "bodegaerp": iinventario
    }

    # Encabezados para la solicitud HTTP
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": APIKEY
    }  
    
    # Realizar la solicitud POST para crear el EPK
    response = requests.post(url, json=payload, headers=headers)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        return JsonResponse({'epk': payload}, status=response.status_code)
    else:
        return JsonResponse({'Error': f'EPK {snumsop} could not be created in WMS'}, status=response.status_code)
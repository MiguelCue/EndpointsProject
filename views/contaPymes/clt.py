from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os

config = load_dotenv()
APIKEY = 'vPRLHH1Bx)gg51-iiza5c#dJ}Lp&e1edjBgbQjX!VUBmMRcNW=9JTQ!3taFmymu%NZy;ki*D]jM630%dA1'


"""
Obtiene la información de un CLT del sistema WMS.

Parámetros:
    request: Objeto HttpRequest que contiene item de la solicitud.

Retorna:
    JsonResponse: Respuesta JSON que contiene la información del cliente si se obtiene con éxito, 
                    o un mensaje de error si la solicitud no es exitosa.
"""
def getclt(request):
    item = request.GET.get('item', None)
    url = 'https://api.copernicowms.com/wms/clt'

    # Si se proporciona el código de ítem, agregarlo a la URL
    if item:
        url += f"?item={item}"
    else:
        # Devolver un mensaje de error si no se proporciona un código de ítem
        return JsonResponse({'Error': 'No item code was provided for filtering'}, status=403)

    # Encabezados para la solicitud HTTP
    headers = {
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    # Realizar la solicitud GET para obtener información del cliente
    response = requests.get(url, headers=headers)
    
    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # Cargar el contenido JSON de la respuesta
        clt = loads(response.content)
        # Verificar si se obtuvo al menos un cliente
        if len(clt) >= 1:
            return JsonResponse({'clt': clt[0]})
        else:
            # Devolver una lista vacía si no se encontró ningún cliente
            return JsonResponse({'clt': []})
    else:
        # Devolver un mensaje de error con el código de estado y el texto de la respuesta
        return JsonResponse({'Error': response.status_code, 'text': response.text})
    

"""
Crea un CLT en el sistema WMS.

Parámetros:
    request: Objeto HttpRequest que contiene la información de la solicitud.

Retorna:
    JsonResponse: Respuesta JSON que indica si el cliente se creó con éxito o no.
"""
def postclt(request):
    # URL del endpoint para crear un CLT
    url = "https://api.copernicowms.com/wms/clt"
    
    # Encabezados para la solicitud HTTP
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    clt = request.GET.get('clt', {})
    
    # Extraer los campos relevantes del cliente
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

    # Json para la creación del CLT
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

    # Realizar la solicitud POST para crear el cliente
    response = requests.post(url, json=payload, headers=headers)
    # Verificar el estado de la respuesta
    if response.status_code == 200:
        return JsonResponse({'clt': payload}, status=response.status_code)
    else:
        # Devolver un mensaje de error si la creación del cliente no es exitosa
        return JsonResponse({'Error': "Client creation error"}, status = response.status_code)

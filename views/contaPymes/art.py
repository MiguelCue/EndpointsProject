from django.http import JsonResponse
from django.utils import timezone 
from dotenv import load_dotenv
from json import loads
import requests
import os

config = load_dotenv()
APIKEY = 'vPRLHH1Bx)gg51-iiza5c#dJ}Lp&e1edjBgbQjX!VUBmMRcNW=9JTQ!3taFmymu%NZy;ki*D]jM630%dA1'

"""
Obtiene la información del artículo (ART) del sistema WMS.

Parámetros:
    request: Objeto HttpRequest que contiene la información de la solicitud.

Retorna:
    JsonResponse: Respuesta JSON que contiene la información del artículo si se obtiene con éxito, 
                    o un mensaje de error si la solicitud no es exitosa.
"""
def getart(request):
    url = "https://api.copernicowms.com/wms/art"
    productoean = request.GET.get('productoean', None)
    
    # Si se proporciona el código de producto, agregarlo a la URL
    if productoean:
        url += f"?productoean={productoean}"
    else: 
        # Devolver un mensaje de error si no se proporciona un código de producto
        return JsonResponse({'Error': 'No productoean code was provided for filtering'}, status=403)

    # Encabezados para la solicitud HTTP
    headers = {
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    # Realizar la solicitud GET para obtener información del artículo
    response = requests.get(url, headers=headers)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        return JsonResponse({'art': response.json()})
    else:
        # Devolver un mensaje de error con el código de estado y el texto de la respuesta
        return JsonResponse({'Error': response.status_code, 'text': response.text}, status=response.status_code)


"""
Crea un artículo (ART) en el sistema WMS.

Parámetros:
    request: Objeto HttpRequest que contiene la información de la solicitud.

Retorna:
    JsonResponse: Respuesta JSON que indica si el artículo se creó con éxito o no.
"""
def postart(request):
    url = "https://api.copernicowms.com/wms/art"

    # Encabezados para la solicitud HTTP
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    # Obtener el artículo de la solicitud
    art = request.GET.get('art', {})
    
    # Obtener la informacion del articulo
    irecurso = art.get('irecurso', None)
    descripcion = art.get('descripcion', None)
    costo = art.get('costo', None)
    nunidad = art.get('nunidad', None)
    qfactor = art.get('qfactor', None)
    iinventario = art.get('iinventario', None)
    sobservaciones = art.get('sobservaciones', None)
    fechaactual = timezone.now().isoformat()
    
    # Construir el payload para crear el artículo
    payload = {
        "productoean": irecurso,
        "descripcion": descripcion,
        "referencia": irecurso,
        "inventariable": 1,
        "um1": nunidad,
        "presentacion": "",
        "costo": costo,
        "referenciamdc": irecurso,
        "descripcioningles": descripcion,
        "item": irecurso,
        "u_inv": nunidad,
        "grupo": "",
        "subgrupo": "",
        "extension1": "",
        "extension2": "",
        "nuevoean": irecurso,
        "qtyequivalente": None,
        "origencompra": None,
        "tipo": "",
        "factor": qfactor,
        "f120_tipo_item": "",
        "fecharegistro": None,
        "peso": None,
        "bodega": iinventario,
        "procedencia": "",
        "estadotransferencia": 0,
        "volumen": None,
        "proveedor": None,
        "preciounitario": costo,
        "ingredientes": None,
        "instrucciones_de_uso": None,
        "u_inv_p": None,
        "observacion": sobservaciones,
        "controla_status_calidad": None,
        "estado": 1,
        "alergenos": None
    }

    # Realizar una solicitud POST para crear el artículo
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        # Devolver el payload del artículo en formato JSON
        return JsonResponse({'art': payload}, status=response.status_code)
    else:
        # Devolver un mensaje de error si la creación falla
        return JsonResponse({'Error': 'Item creation error'}, status=response.status_code)
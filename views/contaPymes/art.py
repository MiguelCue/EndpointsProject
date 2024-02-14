from django.http import JsonResponse
from django.utils import timezone 
from dotenv import load_dotenv
from json import loads
import requests
import os

config = load_dotenv()
APIKEY = os.getenv('APIKEY')

def getart(request):
    url = "https://api.copernicowms.com/wms/art"
    productoean = request.GET.get('productoean', None)

    if productoean:
        url += f"?productoean={productoean}"

    headers = {
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return JsonResponse({'art': response.json()})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text})


def postart(request):
    url = "https://api.copernicowms.com/wms/art"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": APIKEY
    }

    art = request.GET.get('art', {})
    
    irecurso = art.get('irecurso', None)
    descripcion = art.get('descripcion', None)
    costo = art.get('costo', None)
    nunidad = art.get('nunidad', None)
    qfactor = art.get('qfactor', None)
    iinventario = art.get('iinventario', None)
    sobservaciones = art.get('sobservaciones', None)
    fechaactual = timezone.now().isoformat()
    
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
        "fecharegistro": fechaactual,
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
    #return JsonResponse({'art': payload})
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return JsonResponse({'art': payload})
    else:
        return JsonResponse({'Error': response.status_code, 'text': response.text, 'art': art})
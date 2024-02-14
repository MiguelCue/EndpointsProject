from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os

from views.contaPymes.authentication import authentication

config = load_dotenv()

def getbyordernumber(request):
    keyagent = authentication(request)
    keydata = loads(keyagent.content)
    controlkey = keydata.get('key_agente', None) 

    if controlkey is not None:
        snumsop = request.GET.get('doctoerp', None)
        URLUBICACION = os.getenv("URLUBICACION")
        URLFUNCION = '/TCatOperaciones/"DoExecuteOprAction"/'
        URL = URLUBICACION + URLFUNCION
        IAPP = os.getenv("IAPP")

        datajson = {
            'accion': "LOAD",
            'operaciones': [
                {
                'itdoper': 'ORD1',
                'snumsop': snumsop
                },
            ],
        }

        jsonsend = {
            '_parameters': [datajson, controlkey, IAPP, "0"],
        }

        try:
            response = requests.post(URL, json=jsonsend)
            data = response.json()
            pedido = data.get('result', [])[0].get('respuesta', {}).get('datos', {})
            operationnum = pedido.get('encabezado', {}).get('snumsop', None)
            if operationnum:
                return JsonResponse({'pedido': pedido}, status=200)
            else:
                return JsonResponse({'Error': f'The order {snumsop} does not exist'}, status=500)
        except Exception as e:
            return JsonResponse({'Error': f'Request error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'Error': 'User authentication failed'}, status=403)

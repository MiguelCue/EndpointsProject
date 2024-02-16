from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os

from views.contaPymes.authentication import authentication

config = load_dotenv()

def getbyordernumber(request):
    try:
        # Autenticacion del usuario
        keyagent = authentication(request)
        keydata = loads(keyagent.content)
        controlkey = keydata.get('key_agente', None) 

        if controlkey is not None:
            # Configuracion para el agente de servicios web de ContaPyme
            URLUBICACION = os.getenv("URLUBICACION")
            URLFUNCION = '/TCatOperaciones/"DoExecuteOprAction"/'
            URL = URLUBICACION + URLFUNCION
            IAPP = os.getenv("IAPP")

            # Atributo por el cual se filtra el cliente
            snumsop = request.GET.get('doctoerp', None)

            # Parametros para la ejecucion de la peticion
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
                # Se obtiene la información del pedido de la respuesta
                data = response.json()
                pedido = data.get('result', [])[0].get('respuesta', {}).get('datos', {})
                
                # Se verifica que codigo del pedido no este vacio
                doctoerp = pedido.get('encabezado', {}).get('snumsop', None)
                if doctoerp:
                    return JsonResponse({'pedido': pedido}, status=200)
                else:
                    # No existe el pedido en ContaPyme
                    return JsonResponse({'Error': f'The order {snumsop} does not exist'}, status=500)
            except Exception as e:
                # Ocurre un problema al interpretar la respuesta
                return JsonResponse({'Error': f'Request error: {str(e)}'}, status=500)
        else:
            # La autenticación del usuario falla
            return JsonResponse({'Error': 'User authentication failed'}, status=403)
    except Exception as e:
        # Error inesperado durante la ejecución del código
        return JsonResponse({'Error': f'An unexpected error occurred: {str(e)}'}, status=500)

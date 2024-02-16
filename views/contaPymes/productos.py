from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os

from views.contaPymes.authentication import authentication

config = load_dotenv()

def getproductos(request):
    try:
        # Autenticacion del usuario
        keyagent = authentication(request)
        keydata = loads(keyagent.content)
        controlkey = keydata.get('key_agente', None) 

        if controlkey is not None:
            # Configuracion para el agente de servicios web de ContaPyme
            URLUBICACION = os.getenv("URLUBICACION")
            URLFUNCION = '/TCatElemInv/"GetListaElemInv"/'
            URL = URLUBICACION + URLFUNCION
            IAPP = os.getenv("IAPP")

            # Atributo por el cual se filtra el producto
            irecurso = request.GET.get('irecurso', ())
            
            # Parametros para la ejecucion de la peticion
            datajson = {
                "datospagina": {
                    "cantidadregistros": "200",
                    "pagina": "1"
                },
                "datosfiltro": {
                    "sql":f"irecurso='{irecurso}'"
                },
                
                "ordenarpor": {
                    "nrecurso": "asc"
                }
            }
            jsonsend ={ 
                "_parameters" : [ datajson, controlkey, IAPP ,"0" ] 
            }

            try:
                response = requests.post(URL, json=jsonsend)
                data = response.json()
                if data:
                    # Se obtiene la información del producto de la respuesta
                    producto = data.get('result', [])[0].get('respuesta', {}).get('datos', {})
                    return JsonResponse({'producto': producto})
                else:
                    # No hay datos en la respuesta
                    return JsonResponse({'Error': 'No data'}, status=500)
            except Exception as e:
                # Ocurre un problema al interpretar la respuesta
                return JsonResponse({'Error': f'Request error: {str(e)}'}, status=500)
        else:
            # La autenticación del usuario falla
            return JsonResponse({'Error': 'User authentication failed'}, status=403)
    except Exception as e:
        # Error inesperado durante la ejecución del código
        return JsonResponse({'Error': f'An unexpected error occurred: {str(e)}'}, status=500)


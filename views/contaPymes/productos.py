from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os

from views.contaPymes.authentication import authentication

config = load_dotenv()

def getproductos(request):
    keyagent = authentication(request)
    if keyagent.status_code == 200:   
        keydata = loads(keyagent.content)
        controlkey = keydata.get('key_agente', None) 

        if controlkey is not None:
            URLUBICACION = os.getenv("URLUBICACION")
            URLFUNCION = '/TCatElemInv/"GetListaElemInv"/'
            URL = URLUBICACION + URLFUNCION
            IAPP = os.getenv("IAPP")

            irecurso = request.GET.get('irecurso', ())
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

            response = requests.post(URL, json=jsonsend)

            try:
                data = response.json()
                if data:
                    producto = data.get('result', [])[0].get('respuesta', {}).get('datos', {})
                    return JsonResponse({'producto': producto})
                else:
                    return JsonResponse({'Error': 'No data'}, status=500)
            except Exception as e:
                return JsonResponse({'Error': f'Request error: {str(e)}'}, status=500)


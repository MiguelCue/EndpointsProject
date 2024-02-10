from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os

from views.contaPymes.authentication import authentication

config = load_dotenv()

def getclientes(request):
    keyagent = authentication(request)
    init = request.GET.get('init', None)
    
    if keyagent.status_code == 200:       
        keydata = loads(keyagent.content)
        controlkey = keydata.get('key_agente', None) 

        if controlkey is not None:
            URLUBICACION = os.getenv("URLUBICACION")
            URLFUNCION = '/TCatTerceros/"GetInfoTercero"/'
            URL = URLUBICACION + URLFUNCION
            IAPP = os.getenv("IAPP")

            datajson = {
                "init": init
            }

            jsonsend ={ 
                "_parameters" : [ datajson, controlkey, IAPP ,"0" ] 
            }

            response = requests.post(URL, json=jsonsend)

            try:
                data = response.json()
                if data:
                    cliente = data.get('result', [])[0].get('respuesta', {}).get('datos', {})
                    return JsonResponse({'cliente': cliente})
                else:
                    return JsonResponse({'Error': 'No data'}, status=500)
            except Exception as e:
                return JsonResponse({'Error': f'Request error: {str(e)}'}, status=500)


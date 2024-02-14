from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os

from views.contaPymes.authentication import authentication

config = load_dotenv()

def getoperaciones(request):
    keyagent = authentication(request)
    if keyagent.status_code == 200:   
        
        keydata = loads(keyagent.content)
        controlkey = keydata.get('key_agente', None) 

        if controlkey is not None:

            URLUBICACION = os.getenv("URLUBICACION")
            URLFUNCION = '/TCatOperaciones/"GetListaOperaciones"/'
            URL = URLUBICACION + URLFUNCION
            IAPP = os.getenv("IAPP")

            # datajson = {
            #     "datospagina": {
            #         "cantidadregistros": "20",
            #         "pagina": "1"
            #     },
            #     "camposderetorno": [
            #         "itdoper",
            #         "inumoper",
            #         "tdetalle",
            #         "fcreacion",
            #         "ncorto",
            #         "iestado",
            #         "ntdsop",
            #         "ntercero",
            #         "iprocess",
            #         "fsoport",
            #         "snumsop",
            #         "qerror",
            #         "qwarning",
            #         "banulada",
            #         "mingresos",
            #         "megresos",
            #         "mtotaloperacion"
            #     ],
            #     "itdoper": [
            #         "ORD1"
            #     ]
            # }
                

            # jsonsend ={ 
            #     "_parameters" : [ datajson, controlkey, IAPP ,"0" ] 
            # }

            jsonsend = {
            "_parameters": [
                {
                    "datospagina": {
                        "cantidadregistros": "20",
                        "pagina": "1"
                    },
                    "camposderetorno": [
                        "itdoper",
                        "inumoper",
                        "tdetalle",
                        "fcreacion",
                        "ncorto",
                        "iestado",
                        "ntdsop",
                        "ntercero",
                        "iprocess",
                        "fsoport",
                        "snumsop",
                        "qerror",
                        "qwarning",
                        "banulada",
                        "mingresos",
                        "megresos",
                        "mtotaloperacion"
                    ],
                    "ordenarpor": {
                        "fsoport": "desc"
                    },
                    "datosfiltro": {},
                    "itdoper": [
                        "ORD1"
                    ]
                },
                controlkey,
                IAPP,
                "0"
                ]
            }


            response = requests.post(URL, json=jsonsend)

            try:
                data = response.json()
                if data:
                    return JsonResponse({'data': data})
                else:
                    return JsonResponse({'Error': 'No data'}, status=500)
            except Exception as e:
                return JsonResponse({'Error': f'Request error: {str(e)}'}, status=500)


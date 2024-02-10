from json import loads
from django.http import JsonResponse
from views.connekta_siesa.peticiones.conectores_importar import conectores_importar

def requesicion2(_):
    payload = {
        "Inicial": [
            {
            "F_CIA": "1"
            }
        ],
        "Final": [
            {
            "F_CIA": "1"
            }
        ],
        "Documentos": [
            {
            "F_CIA": "1",
            "f350_id_co": "001",
            "f350_id_tipo_docto": "TI",
            "f350_consec_docto": "0",
            "f350_fecha": "20240203",
            "f440_id_co_req_int": "001",
            "f440_id_tipo_docto_req_int": "RQI",
            "f440_consec_docto_req_int": "6",
            "f450_docto_alterno": ""
            }
        ]
    }
        
    return JsonResponse({'payload': payload})
    







    
        
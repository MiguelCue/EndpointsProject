from json import loads
from django.http import JsonResponse
from views.connekta_siesa.peticiones.conectores_importar import conectores_importar

def requesicion3(_):
    payload = {
        "Inicial": [
            {
            "F_CIA": "1"
            }
        ],
        "Compromisos": [
            {
            "F_CIA": "1",
            "f430_id_co": "001",
            "f430_id_tipo_docto": "PV",
            "f430_consec_docto": "7268",
            "f431_id_item": "2103",
            "f431_referencia_item": "",
            "f431_id_ext1_detalle": "",
            "f431_id_ext2_detalle": "",
            "f431_id_bodega": "L006",
            "f431_id_ubicación_aux": "",
            "f431_id_lote": "WOP10961-231103",
            "f431_id_unidad_medida": "m2",
            "f431_cant_base": "1",
            "f431_nro_registro": "24750"
            }
        ],
        "Final": [
            {
            "F_CIA": "1"
            }
        ]
    }

    return JsonResponse({'payload': payload})
    
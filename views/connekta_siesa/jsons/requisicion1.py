from json import loads
from django.http import JsonResponse

from views.connekta_siesa.peticiones.conectores_importar import conectores_importar

def requesicion1(_):
    comp_req = conectores_importar(_)
    data_requisicion = loads(comp_req.content).get('data', {})[0]
    if data_requisicion:
        
        payload = {
            "Inicial": [
                {
                "F_CIA": "1"
                }
            ],
            "Compromisos": [
                {
                "F_CIA": "1",
                "f440_id_co": "001",
                "f440_id_tipo_docto": "RQI",
                "f440_consec_docto": "6",
                "f441_id_item": "80",
                "f441_referencia_item": "MP00080",
                "f441_id_ext1_detalle": "",
                "f441_id_ext2_detalle": "",
                "f441_id_bodega": "L002",
                "f441_id_ubicación_aux": "",
                "f441_id_lote": "230919A09A",
                "f441_id_unidad_medida": "Kg",
                "f441_cant_base": "1",
                "f441_id_bodega_ent": "P001",
                "f441_id_ubicación_aux_ent": "",
                "f441_id_lote_ent": "230919A09A",
                "f441_cant_por_remisionar_base": "1",
                "f441_nro_registro": "14"
                }
            ],
            "Final": [
                {
                "F_CIA": "1"
                }
            ]
        }

        return JsonResponse({'payload': payload})
    return JsonResponse({'Error': 'Error loading purchase information'})








    
        
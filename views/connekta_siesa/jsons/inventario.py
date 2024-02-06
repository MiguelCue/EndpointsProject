from json import loads
from django.http import JsonResponse
from views.connekta_siesa.peticiones.conectores_importar import conectores_importar

def inventario(_):
    entinv = conectores_importar(_)
    data_inventario = loads(entinv.content).get('data', {})[0]
    if data_inventario:
        payload = {
            "Inicial": [
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
                "f350_id_tercero": "",
                "f350_notas": "Prueba",
                "f450_id_bodega_salida": "L002",
                "f450_id_bodega_entrada": "P002",
                "f450_docto_alterno": "",
                "f350_fecha" : "20240201"
                }
            ],
            "Movimientos": [
                {
                "F_CIA": "1",
                "f470_id_co": "001",
                "f470_id_tipo_docto": "TI",
                "f470_consec_docto": "0",
                "f470_nro_registro": "1",
                "f470_id_bodega": "L002",
                "f470_id_ubicación_aux": "",
                "f470_id_lote_ent" : "230919A09A",
                "f470_id_lote": "230919A09A",
                "f470_id_motivo": "01",
                "f470_id_co_movto": "001",
                "f470_id_ccosto_movto": "",
                "f470_id_unidad_medida": "kg",
                "f470_cant_base": "1",
                "f470_costo_prom_uni": "",
                "f470_id_item": "80",
                "f470_referencia_item": "MP00080",
                "f470_id_ext1_detalle": "",
                "f470_id_ext2_detalle": "",
                "f470_id_un_movto": "99"
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








    
        


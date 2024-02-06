from json import loads
from django.http import JsonResponse
from views.connekta_siesa.peticiones.validar_entrada_compra import validar_entrada_compra

def generar_recibo(request):
    entrada_compra = validar_entrada_compra(request)
    data_compra = loads(entrada_compra.content).get('data', {})[0]
    if data_compra:
        id_comprador = data_compra.get('id_comprador', None)
        id_proveedor = data_compra.get('id_proveedor', None)

        payload = {
            "Inicial":[
                {
                    "F_CIA":"1"
                }
            ],
            "Documentos":[
                {
                    "F_CIA":"1",
                    "f350_id_co":"001",
                    "f350_id_tipo_docto":"EA",
                    "f350_consec_docto":"0",
                    "f350_fecha":"20240205",
                    "f350_id_tercero":id_comprador,
                    "f350_notas":"Prueba",
                    "f451_id_sucursal_prov":"001",
                    "f451_id_tercero_comprador":id_proveedor,
                    "f451_num_docto_referencia":"181",
                    "f451_id_moneda_docto":"COP",
                    "f451_id_moneda_conv":"COP",
                    "f420_id_co_docto":"001",
                    "f420_id_tipo_docto":"OCI",
                    "f420_consec_docto":"181"
                }
            ],
            "Movimientos":[
                {
                    "F_CIA":"1",
                    "f470_id_co":"001",
                    "f470_id_tipo_docto":"EA",
                    "f470_consec_docto":"0",
                    "f470_nro_registro":"1",
                    "f470_id_bodega":"L003",
                    "f470_id_ubicacion_aux":"",
                    "f470_id_lote":"20240205",
                    "f470_id_unidad_medida":"und",
                    "f421_fecha_entrega":"20240205",
                    "f470_cant_base":"3",
                    "f470_id_item":"4943",
                    "f470_referencia_item":"0004943",
                    "f470_id_ext1_detalle":"",
                    "f470_id_ext2_detalle":"",
                    "f470_rowid":"31145"
                }
            ],
            "Final":[
                {
                    "F_CIA":"1"
                }
            ]
        }

        return JsonResponse({'payload': payload})
    return JsonResponse({'Error': 'Error loading purchase information'})








    
        
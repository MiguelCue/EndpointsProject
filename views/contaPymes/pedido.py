from django.http import JsonResponse
from json import loads
from views.contaPymes.dpk import getdpk, postdpkV2

from views.contaPymes.epk import getepk, postepkV2
from views.contaPymes.inventoryOperation import getbyordernumber


"""
    Maneja la solicitud de orden y realiza las operaciones necesarias en función de la información proporcionada.

    Parámetros:
        request: Objeto HttpRequest que contiene la información de la solicitud.

    Retorna:
        JsonResponse: Respuesta JSON que indica el resultado de la operación.
"""
def createpedido(request):
    new_request = type('Request', (), {})()
    # Obtener el número de documento de ERP de la solicitud
    doctoerp = request.GET.get('doctoerp', None)
    
    # Verificar si existe el pedido asociado al doctoerp en ContaPyme
    pedidojson = getbyordernumber(request)
    pedido = loads(pedidojson.content).get('pedido', {})
    if not pedido:
        return JsonResponse({'Error': f'The order {doctoerp} does not exist in ContaPymes'}, status=500)
    
    # Verificar si la bodega es la que se maneja con el WMS
    bodega = pedido.get("datosprincipales", {}).get("iinventario", None)
    if bodega == '10':
        # Verificar si el EPK asociado al doctoerp no se encuentre creado
        epkjson = getepk(request)
        epk = loads(epkjson.content).get('epk', {})
        if not epk:
            # Configurar la solicitud con la información pedido
            setattr(new_request, 'GET', {'pedido': pedido})
            
            # Creacion el EPK en el WMS
            epkjson = postepkV2(new_request)
            if epkjson.status_code == 200:
                epk = loads(epkjson.content).get('epk', {})
            else:
                return JsonResponse({'Error': f'EPK {doctoerp} could not be created in WMS'}, status=epkjson.status_code)    

        # Verificar si el DPK asociado al doctoerp no se encuentre creado
        dpkjson = getdpk(request)
        dpk = loads(dpkjson.content).get('dpk', {})
        if not dpk:
            # Obtener el numero del picking del epk
            picking = _getpicking(request)
            
            # Configurar la solicitud con la información del picking, pedido y EPK
            setattr(new_request, 'GET', {'picking': picking, 'pedido': pedido, 'epk': epk})
            dpkjson = postdpkV2(new_request)

            # Creacion del DPK en el WMS
            if dpkjson.status_code == 200:
                return JsonResponse({'Success': f'EPK and DPK {doctoerp} created in WMS'}, status=200) 
            else:
                return JsonResponse({'Error': f'DPK {doctoerp} could not be created in WMS'}, status=500)
        else:
            return JsonResponse({'Error': f'DPK {doctoerp} already exist in WMS'}, status=500)
    else:
        return JsonResponse({'Error': f'The order {doctoerp} belongs to another store'}, status=500)    
    
      
"""
    Obtiene el numero del picking asociado a una solicitud.

    Parámetros:
        request: Objeto HttpRequest que contiene la información de la solicitud.

    Retorna:
        picking: Información del picking asociado a la solicitud.

"""
def _getpicking(request):
    # Obtener información del EPK asociado al doctoerp de la solicitud
    epkjson = getepk(request)
    epk = loads(epkjson.content).get('epk', {})
    # Obtener el picking del EPK
    picking = epk.get('picking', None)
    return picking
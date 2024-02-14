from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dotenv import load_dotenv
from json import loads
import requests
import os
from views.contaPymes.dpk import getdpk

from views.contaPymes.epk import getepk, postepk

config = load_dotenv()

@csrf_exempt
def createpedido(request):
    epkjson = getepk(request)
    epk = loads(epkjson.content).get('epk', {})
    clt = {}
    if not epk:
        epkjson = postepk(request)
        epk = loads(epkjson.content).get('epk', {})
        clt = loads(epkjson.content).get('clt', {})
         
    dpkjson = getdpk(request)
    
    dpk = loads(dpkjson.content).get('dpk', {})

    if dpk:
        return JsonResponse({'epk': epk,
                         'clt': clt,
                         'dpk': dpk,})
    else:
        return JsonResponse({'error': 'error'})
    
    
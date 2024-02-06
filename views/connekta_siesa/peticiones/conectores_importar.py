from dotenv import load_dotenv
from django.http import JsonResponse
import requests
import os

config = load_dotenv()

def conectores_importar(request):
    idcompania = request.GET.get('idCompania', None)
    idinterface = request.GET.get('idInterface', None)
    iddocumento = request.GET.get('idDocumento', None)
    nombredocumento = request.GET.get('nombreDocumento', None)
    
    URL = "https://connektaqa.siesacloud.com/api/v3/conectoresimportar"

    if idcompania:
        URL +=  f"?idCompania={idcompania}"

    if idinterface:
        URL += f"&idInterface={idinterface}"

    if iddocumento:
        URL += f"&idDocumento={iddocumento}"

    if nombredocumento:
        URL += f"&nombreDocumento={nombredocumento}"

    headers = {
        'Authorization': os.getenv("APIKEYSIESA")
    }

    response = requests.get(URL, headers=headers)

    try:
        data = response.json()
        if data:
            return JsonResponse({'idCompania': idcompania,
                         'idInterface': idinterface,
                         'idDocumento': iddocumento,
                         'nombreDocumento': nombredocumento,
                         'Url': URL
            })
        else:
            return JsonResponse({'Error': 'No data'}, status=500)
    except Exception as e:
        return JsonResponse({'Error': f'Request error: {str(e)}'}, status=500)
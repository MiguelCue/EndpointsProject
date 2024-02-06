from dotenv import load_dotenv
from django.http import JsonResponse
import requests
import os

config = load_dotenv()

def validar_entrada_compra(request):

    parametros = request.GET.get('parametros', None)
    description = request.GET.get('description', None)

    URL = "https://api.copernicowms.com/connekta_siesa/query"

    if parametros:
        URL += f'?parametros={parametros}'

    if description:
        URL += f'&description={description}'

    headers = {
        'Authorization': os.getenv("APIKEYSIESA")
    }
    
    response = requests.get(URL, headers=headers)

    try:
        data = response.json()
        if data:
            return JsonResponse({'data': data})
        else:
            return JsonResponse({'Error': 'No data'}, status=500)
    except Exception as e:
        return JsonResponse({'Error': f'Request error: {str(e)}'}, status=500)
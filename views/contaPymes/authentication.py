from dotenv import load_dotenv
from django.http import JsonResponse
import requests
import os

config = load_dotenv()

def authentication(_):
    URLUBICACION = os.getenv("URLUBICACION")
    URLFUNCION = '/TBasicoGeneral/"GetAuth"/'
    URL = URLUBICACION + URLFUNCION
    IAPP = os.getenv("IAPP")

    datajson = {
        'email': os.getenv("EMAIL"),
        'password': os.getenv("PASSWORD"),
        'idmaquina': '',
    }

    jsonsend = {
        '_parameters': [datajson, '', IAPP, '0'],
    }

    response = requests.post(URL, json=jsonsend)

    try:
        if response.status_code == 200:
            data = response.json()
            result = data.get('result', [])
            if result:
                response = result[0].get('respuesta', {}).get('datos', {})
                controlkey = response.get('keyagente', '')
                return JsonResponse({'key_agente': controlkey})
            else:
                return JsonResponse({'Error': 'No result'}, status=500)
        else:
            return JsonResponse({'Error': f'Request error: {response.status_code}'}, status=500)
    except Exception as e:
        return JsonResponse({'Error': f'Request error: {str(e)}'}, status=500)
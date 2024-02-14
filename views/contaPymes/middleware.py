import os

APIKEY = 'vPRLHH1Bx)gg51-iiza5c#dJ}Lp&e1edjBgbQjX!VUBmMRcNW=9JTQ!3taFmymu%NZy;ki*D]jM630%dA1'
#APIKEY = os.getenv('APIKEY')


def __call__(self, request):
    # API kEY esperada
    expected_api_key = APIKEY
    # Obtenemos la API key que llega en la solicitud HTTP
    api_key = request.META.get('HTTP_API_KEY')

    # Comparamos la API key de la solicitud con la esperada
    if api_key != expected_api_key:
        return JsonResponse({'error': 'API Key inválida'}, status=403)

    # Si la API key es válida, continuamos con la solicitud
    response = self.get_response(request)
    return response
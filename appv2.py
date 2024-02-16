from json import loads
from time import sleep
import threading
import requests

def process_requests(start_i):
    i = start_i
    while True:
        try:
            URL = f'http://127.0.0.1:8000/createpedido?doctoerp=PED-{i}'
            print(URL)

            response = requests.get(URL)
            print(response)

            if response.status_code == 200:
                i += 1
                sleep(10)
            else:
                error = loads(response.content).get('Error')
                if error == f'The order PED-{i} does not exist in ContaPymes':
                    print('contapyme')
                    sleep(120)
                elif error == f'The order PED-{i} belongs to another store':
                    i += 1
                    print('store')
                elif error == f'DPK PED-{i} already exist in WMS':
                    i += 1
                    print('WMS')
                else:
                    return response.text

        except Exception as e:
            print(e)
            break
        
# Inicia un hilo para procesar las solicitudes
thread = threading.Thread(target=process_requests, args=(44735,))
thread.start()

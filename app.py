import requests
if __name__ == "__main__":
    
    c = '44599'
    d = '44700'
    # while True:
    # for i in array:
    for i in range(int(c), int(d)):
        try:
            URL = f'http://127.0.0.1:8000/epk/post?doctoerp=PED-{i}'
            print(URL)

            response = requests.get(URL)
            print(response)

            URL = f'http://127.0.0.1:8000/dpk/post?doctoerp=PED-{i}'
            print(URL)

            response = requests.get(URL)
            print(response)
        except Exception as e:
            print(e)
            break
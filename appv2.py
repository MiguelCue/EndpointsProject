import requests
import threading
from time import sleep

orden = 44638

def automatic():
    global orden
    #while True:
    for i in range(10):
        print(orden)
        orden += 1
        sleep(10)

t1 = threading.Thread(target=automatic)
t1.start()

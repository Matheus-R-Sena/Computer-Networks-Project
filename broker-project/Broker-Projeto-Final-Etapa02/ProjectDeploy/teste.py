import random
import time
numero = 3


while True:

    numero_aleatorio = random.randint(1,3)

    if numero_aleatorio == 1:
        print("nublado")


    elif numero_aleatorio == 2:
        print("ensolarado")


    elif numero_aleatorio == 3:
        print("nublado")
    
    time.sleep(numero)

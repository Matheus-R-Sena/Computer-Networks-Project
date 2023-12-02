#Temperatura simulador 
"""
Este publisher irá simular uma atualização do Clima, enviando novos dados a respeito das condições climáticas entre chuvoso, ensolarado
e nublado.
"""

import random
import socket
import sys
import time


def Publica (numero, cliente):

    while True:
        numero_aleatorio = random.randint(-40,60)


        
        # Colocando o marcador publicar para o broker 
        comando = f"{numero_aleatorio}"

        print(comando)

        #envia comando com o marcador
        cliente.send(comando.encode())


        time.sleep(numero)
        

#Estabelecimento da conexão

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Função usada para conectar ao servidor
cliente.connect(('127.0.0.1', 9000))

comando = "publicar Temperatura"

cliente.send(comando.encode())

print("Conexão realizada com sucesso com o servidor")

numero = int(sys.argv[1])

Publica(numero, cliente)
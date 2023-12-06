#Temperatura simulador 
"""
Este publisher irá simular uma atualização da temperatura
"""

import random
import socket
import sys
import time


def Publica (numero, cliente):

    while True:
        numero_aleatorio = random.randint(0,60)


        
        # Colocando o marcador publicar para o broker 
        comando = f"{numero_aleatorio}"
        Cliente_end, Cliente_porta = cliente.getpeername()
        print("________________________________________________________________________________________________________")
        print(f'Enviando dado: {comando} para IP {Cliente_end} e porta {Cliente_porta}')

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
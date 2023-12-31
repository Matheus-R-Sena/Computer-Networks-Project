#Clima simulador 
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
        numero_aleatorio = random.randint(1,3)

        if numero_aleatorio == 1:
            mensagem = "nublado"

        
        elif numero_aleatorio == 2:
            mensagem = "ensolarado"

        
        elif numero_aleatorio == 3:
            mensagem = "chuvoso"


        
        # Colocando o marcador publicar para o broker 
        comando = f"{mensagem}"

        Cliente_end, Cliente_porta = cliente.getpeername()
        print("________________________________________________________________________________________________________")
        print(f'Enviando dado: {comando} para IP {Cliente_end} e porta {Cliente_porta}')

        #envia dado para o 
        cliente.send(comando.encode())


        time.sleep(numero)
        

#Estabelecimento da conexão

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Função usada para conectar ao servidor
cliente.connect(('127.0.0.1', 9000))

#Envia o comando para acessar o método no broker e o tópico
comando = "publicar Clima"

cliente.send(comando.encode())

print("Conexão realizada com sucesso com o servidor")

numero = int(sys.argv[1])

Publica(numero, cliente)

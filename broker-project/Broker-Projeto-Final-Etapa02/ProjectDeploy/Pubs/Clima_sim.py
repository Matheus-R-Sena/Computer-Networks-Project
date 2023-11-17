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

        print(mensagem)

        #envia comando com o marcador
        cliente.send(comando.encode())

        # recebe uma mensagem de confirmação do servidor
        #confirmacao = cliente.recv(1024).decode()

        # verifica a mensagem de confirmação 
        #if confirmacao == "publicacao confirmada":

        #    print("\n\npublicacao confirmada\n\n")
        

        #else:
        #   print("falha ao publicar mensagem no tópico")


        # encerra a conexão com o servidor

        time.sleep(numero)
        

#Estabelecimento da conexão

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Função usada para conectar ao servidor
cliente.connect(('127.0.0.1', 9000))

comando = "publicar"

cliente.send(comando.encode())

print("Conexão realizada com sucesso")

numero = int(sys.argv[1])

Publica(numero, cliente)

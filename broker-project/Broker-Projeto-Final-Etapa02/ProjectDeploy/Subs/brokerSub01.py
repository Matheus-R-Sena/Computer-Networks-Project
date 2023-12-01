
#Bibliotecas Utilizadas
import socket
import argparse

def assinar(cliente, topico):

    
    #Enviando comando e tópicos para o broker
    comando = "assinar " + "".join(topico)
    cliente.send(comando.encode())


    while True:
        mensagem = cliente.recv(1024).decode()
        print(mensagem)


   
    
    



#Setup da conexão
try:

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # cria um objeto socket para o Sub
    cliente.connect(('127.0.0.1', 9000)) 
    #Utilizamos o comando connect do objeto socket "cliente" para fazer a conexão com o servidor a partir de seus endereços de IP e porta

    print("\nConexão estabelecida com o Servidor\n")

except Exception as e:
    print(f"Falha ao se conectar com o servidor {e} \n\n Por favor verifique o status do servidor")

    
# Comandos no Terminal


argumentos = argparse.ArgumentParser(description = "modulo brokerSub")
argumentos.add_argument("-t", help = "topico", required = True)
entrada = argumentos.parse_args()

"""Estamos colocando o Sub para receber apenas um tópico
"""
#Chamada do método assinar
assinar(cliente, entrada.t)


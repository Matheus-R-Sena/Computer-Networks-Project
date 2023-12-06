# Cliente Clima
#Bibliotecas Utilizadas
import socket
import argparse

def assinar(cliente, topico, clienteDash):

    
    #Enviando comando e tópicos para o broker
    comando = "assinar " + "".join(topico)
    cliente.send(comando.encode())

    #Pegando IP e porta do broker
    Cliente_end, Cliente_porta = cliente.getpeername()

    #Enviando comando Clima para o dashboard
    print("Cheguei até aqui")
    msg = "Clima"
    clienteDash.send(msg.encode())
    #Pegando IP e porta do broker
    ClienteDash_end, ClienteDash_porta = clienteDash.getpeername()

    while True:
        #Recebe do broker
        mensagem = cliente.recv(1024).decode()
        print("________________________________________________________________________________________________________")
        print(f'Recebendo dado: {mensagem} do Broker IP {Cliente_end} e porta {Cliente_porta} e enviando para dashboard IP {ClienteDash_end} e porta {ClienteDash_porta}')
       
        #Manda para o Dash
        clienteDash.send(mensagem.encode())
        


   
    
    



#Setup da conexão
try:
    #Socket Cliente do Broker
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # cria um objeto socket para o Sub
    cliente.connect(('127.0.0.1', 9000)) 
    #Utilizamos o comando connect do objeto socket "cliente" para fazer a conexão com o servidor a partir de seus endereços de IP e porta
    print("\nConexão estabelecida com o Broker\n")

    #Socket Cliente do Dashboard
    clienteDash = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # cria um objeto socket para o Sub
    clienteDash.connect(('127.0.0.1', 10000)) 
    #Utilizamos o comando connect do objeto socket "cliente" para fazer a conexão com o servidor a partir de seus endereços de IP e porta
    print("\nConexão estabelecida com o Dashboard\n")

except Exception as e:
    print(f"Falha ao se conectar com o servidor {e} \n\n Por favor verifique o status do servidor")

    
# Comandos no Terminal


argumentos = argparse.ArgumentParser(description = "modulo brokerSub")
argumentos.add_argument("-t", help = "topico", required = True)
entrada = argumentos.parse_args()

"""Estamos colocando o Sub para receber apenas um tópico
"""
#Chamada do método assinar
assinar(cliente, entrada.t, clienteDash)


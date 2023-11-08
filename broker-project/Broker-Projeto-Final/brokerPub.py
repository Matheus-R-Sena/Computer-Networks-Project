import socket
import argparse

# configuração dos argumentos da linha de comando
argumentos = argparse.ArgumentParser(description = "modulo brokerPub")
argumentos.add_argument("-t", help = "tópico", required = True)
argumentos.add_argument("-m", nargs = "+", help = "mensagem", required = True)
entrada = argumentos.parse_args()


topico = entrada.t
mensagem = entrada.m


    #Conexão com o servidor
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Função usada para conectar ao servidor
    cliente.connect(('127.0.0.1', 9000))

    # Enviando mensagem 
    comando = f"publicar {topico} {mensagem}"
    cliente.send(comando.encode())

    # recebe uma mensagem de confirmação do servidor
    confirmacao = cliente.recv(1024).decode()

    # verifica a mensagem de confirmação 
    if confirmacao == "publicacao confirmada":

        print(f"Mensagem: '{mensagem}' Tópico: '{topico}'")

    else:
        print("falha ao publicar mensagem no tópico")


# encerra a conexão com o servidor
finally:
    cliente.close()

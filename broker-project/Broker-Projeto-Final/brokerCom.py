import socket       # biblioteca para estabelecer as conexões
import argparse     # biblioteca para configurar os argumentos da linha de comando

#função para utilizar comandos de controle 
def comandos(comando):


    # criando objeto socket para o cliente se conectar com o servidor
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 9000))

    # verificação do comando 
    if comando == "LIST":

        # envia o comando para o servidor broker
        cliente.send("list".encode())

        # recebe uma mensagem de confirmação do servidor
        confirmacao = cliente.recv(1024).decode()
    
        # verifica a mensagem de confirmação
        print(f"Confirmação: {confirmacao}")
        if confirmacao == "confirmado":

            print("Comando aceito! Confira abaixo a lista de tópicos e seus assinantes:") 

            # O código recebe uma lista de tópicos e assinantes do servidor, 
            lista = cliente.recv(1024).decode()
            
            print(lista)  # imprime a lista mantida e enviada pelo broker
            
            
        else:
            print("Comando não aceito pelo servidor")

    # caso o comando utilizado nao for o -c LIST ele imprimirá um erro
    else:
        print("Erro ao imprimir a lista, por favor utilize o comando: -c LIST")


# encerra a conexão com o servidor



# configuração dos argumentos da linha de comando
argumentos = argparse.ArgumentParser(description = "modulo brokerCom")
argumentos.add_argument("-c", help = "comando", required = True)
entrada = argumentos.parse_args()
comandos(entrada.c)

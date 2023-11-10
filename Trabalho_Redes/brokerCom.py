import socket       # biblioteca para estabelecer as conexões
import argparse     # biblioteca para configurar os argumentos da linha de comando


# Argumentos da linha de comando (configuração)
argumentos = argparse.ArgumentParser(description="modulo brokerCom")
argumentos.add_argument("-c", help="comando", required=True)
entrada = argumentos.parse_args()


comando = entrada.c

# criando objeto socket para o cliente se conectar com o servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 9000))

# verificação do comando
if comando == "LIST":

    # enviando o comando
    cliente.send("list".encode())

    # recebendo confirmação
    confirmacao = cliente.recv(1024).decode()

    # verificando mensagem
    print(f"Confirmação: {confirmacao}")
    if confirmacao == "confirmado":

        print("Comando aceito! Tópicos e seus assinantes:")

        # Recebendo uma lista de tópicos e assinantes do broker
        lista = cliente.recv(1024).decode()

        print(lista)

    else:
        print("Comando não aceito")

else:
    print("Erro ao acessar a lista.")


cliente.close()

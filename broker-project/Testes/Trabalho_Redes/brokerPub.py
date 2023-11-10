import socket
import argparse

# configuração dos argumentos da linha de comando
argumentos = argparse.ArgumentParser(description="modulo brokerPub")
argumentos.add_argument("-t", help="tópico", required=True)
argumentos.add_argument("-m", nargs="+", help="mensagem", required=True)
entrada = argumentos.parse_args()


topico = entrada.t
mensagem = entrada.m


# Configuração para a conexão
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 9000))

# Enviando mensagem
comando = f"publicar {topico} {mensagem}"
cliente.send(comando.encode())

# Confirmando
confirmacao = cliente.recv(1024).decode()

# verificando confirmação
if confirmacao == "publicacao confirmada":

    print(f"Tópico: '{topico}' Mensagem: '{mensagem}'")

else:
    print("falha na publicação")


# fim da conexão com o servidor
cliente.close()

import socket
import argparse

# estrutura para envio de comando
parser = argparse.ArgumentParser(description="Broker Subscriber")
parser.add_argument("-t", nargs='+', required=True, help="Lista de topicos")
args = parser.parse_args()

topicos = args.t

# cria um objeto socket para o Sub
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 9000))  # conexão do cliente com o servidor
# Utilizamos o comando connect do objeto cliente para fazer a conexão com o servidor a partir de seus endereços de IP e porta

comando = f"assinar " + " ".join(topicos)
cliente.send(comando.encode())  # envia comando para broker
print(comando)  # imprime o comando

# recebe mensagem de confirmação do cliente
confirmacao = cliente.recv(1024).decode()


if confirmacao == "assinatura confirmada":
    print("Assinatura realizada com sucesso")

    # Loop onde o Sub fica a espera de publicações nos tópicos em que está
    while True:

        dado = cliente.recv(1024).decode()
        if (dado != "assinatura confirmada" and dado != "Assinatura realizada"):
            info = dado.split()
            mensagem = info[0]
            topico = info[1]
            print(f"Topico: {topico} Mensagem: {mensagem}")
        else:
            print(dado)

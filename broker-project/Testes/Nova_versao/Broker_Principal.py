import socket
import threading

# Dicionário para armazenar os tópicos e seus assinantes
topicos_assinantes = {}

# Função para receber e processar mensagens de clientes
def handle_client(client):
    while True:
        data = client.recv(1024)
        if not data:
            break

        comando, *params = data.decode().split()
        print(f"Comando recebido: {comando} Parâmetros: {params}")

        if comando == "subscribe":
            if len(params) >= 2:
                topico, mensagem = params[0], " ".join(params[1:])
                assinar(client, topico)
        elif comando == "publish":
            if len(params) >= 2:
                topico, mensagem = params[0], " ".join(params[1:])
                publicar(client, topico, mensagem)
        elif comando == "list":
            listar_topicos(client)

        client.sendall("COMANDO_CONFIRMATION_ACK".encode())  # Mensagem de confirmação

# Função para assinar um tópico
def assinar(client, topico):
    if topico not in topicos_assinantes:
        topicos_assinantes[topico] = []

    topicos_assinantes[topico].append(client)

    client.sendall("assinatura confirmada".encode())  # Mensagem de confirmação

# Função para publicar uma mensagem
def publicar(client, topico, mensagem):
    if topico in topicos_assinantes:
        for assinante in topicos_assinantes[topico]:
            assinante.sendall(f"{topico} {mensagem}".encode())

        client.sendall("publicação confirmada".encode())  # Mensagem de confirmação
    else:
        client.sendall("publicação não confirmada".encode())  # Mensagem de confirmação

# Função para listar os tópicos e seus assinantes
def listar_topicos(client):
    topicos_e_assinantes = {topico: [assinante.getpeername() for assinante in assinantes]
                           for topico, assinantes in topicos_assinantes.items()}
    resposta = str(topicos_e_assinantes)
    client.sendall(f"COMANDO_CONFIRMATION_ACK\n{resposta}\n".encode())

# Configurações do servidor
host = "127.0.0.1"
porta = 8081

# Cria um socket TCP
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket.bind((host, porta))
servidor_socket.listen()

print(f"Servidor ouvindo em: {host}:{porta}")

# Loop para aceitar conexões
while True:
    cliente, endereco = servidor_socket.accept()
    threading.Thread(target=handle_client, args=(cliente,)).start()

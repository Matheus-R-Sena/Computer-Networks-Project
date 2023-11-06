import socket  # Importa o módulo 'socket' para comunicação por meio de sockets
import threading  # Importa o módulo 'threading' para lidar com múltiplas conexões de clientes em paralelo

# Dicionário para armazenar os tópicos e seus assinantes
topicos_assinantes = {}

# Função para receber e processar mensagens de clientes
def handle_client(client):
    while True:
        data = client.recv(1024)  # Recebe dados do cliente (até 1024 bytes)
        if not data:
            break

        comando, *params = data.decode().split()  # Divide a mensagem em comando e parâmetros
        print(f"Comando recebido: {comando} Parâmetros: {params}")  # Exibe o comando e parâmetros recebidos

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

        client.sendall("COMANDO_CONFIRMATION_ACK".encode())  # Envia uma mensagem de confirmação ao cliente

# Função para assinar um tópico
def assinar(client, topico):
    if topico not in topicos_assinantes:
        topicos_assinantes[topico] = []

    topicos_assinantes[topico].append(client)

    client.sendall("assinatura confirmada".encode())  # Envia uma mensagem de confirmação ao cliente

# Função para publicar uma mensagem
def publicar(client, topico, mensagem):
    if topico in topicos_assinantes:
        for assinante in topicos_assinantes[topico]:
            assinante.sendall(f"{topico} {mensagem}".encode())

        client.sendall("publicação confirmada".encode())  # Envia uma mensagem de confirmação ao cliente
    else:
        client.sendall("publicação não confirmada".encode())  # Envia uma mensagem de confirmação ao cliente

# Função para listar os tópicos e seus assinantes
def listar_topicos(client):
    topicos_e_assinantes = {topico: [assinante.getpeername() for assinante in assinantes]
                           for topico, assinantes in topicos_assinantes.items()}
    resposta = str(topicos_e_assinantes)
    client.sendall(f"COMANDO_CONFIRMATION_ACK\n{resposta}\n".encode())

# Configurações do servidor
host = "127.0.0.1"  # Endereço IP em que o servidor escuta
porta = 8081  # Número da porta em que o servidor escuta

# Cria um socket TCP
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um objeto de socket TCP
servidor_socket.bind((host, porta))  # Liga o socket ao endereço e porta especificados
servidor_socket.listen()  # Coloca o socket em modo de escuta

print(f"Servidor ouvindo em: {host}:{porta}")  # Exibe a mensagem indicando que o servidor está ouvindo

# Loop para aceitar conexões
while True:
    cliente, endereco = servidor_socket.accept()  # Aceita uma conexão de cliente
    threading.Thread(target=handle_client, args=(cliente,)).start()  # Cria uma nova thread para lidar com o cliegit config --global user.email "seu@email.com"

import socket
import threading

# Dicionário para armazenar os tópicos e seus assinantes
topicosAssinantes = {}

# Função para receber e processar mensagens de clientes
def handle_client(client):
    while True:
        data = client.recv(1024)
        if not data:
            break

        command, *params = data.decode().split()
        print(f"Comando recebido: {command} Parâmetros: {params}")

        if command == "subscribe":
            if params:
                topic = params[0]
                subscribe(client, topic)
        elif command == "publish":
            if len(params) >= 2:
                topic, message = params[0], " ".join(params[1:])
                publish(client, topic, message)
        elif command == "list":
            list_topics(client)

        client.sendall("operation_confirmed".encode())

# Função para assinar um tópico
def subscribe(client, topic):
    if topic not in topicosAssinantes:
        topicosAssinantes[topic] = []

    topicosAssinantes[topic].append(client)

    client.sendall("subscription_confirmed".encode())

# Função para publicar uma mensagem
def publish(client, topic, message):
    if topic in topicosAssinantes:
        for subscriber in topicosAssinantes[topic]:
            subscriber.sendall(f"{topic} {message}".encode())

    client.sendall("publication_confirmed".encode())

# Função para listar os tópicos e seus assinantes
def list_topics(client):
    topics_and_subscribers = {topic: [subscriber.getpeername() for subscriber in subscribers]
                               for topic, subscribers in topicosAssinantes.items()}

    client.sendall(str(topics_and_subscribers).encode())

# Configurações do servidor
host = "127.0.0.1"
port = 8080

# Cria um socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Servidor ouvindo em: {host}:{port}")

# Loop para aceitar conexões
while True:
    client, address = server_socket.accept()
    threading.Thread(target=handle_client, args=(client,)).start()


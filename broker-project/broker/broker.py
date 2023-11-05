#Programa broker

"""
Comentários simplificados para auxiliar no desenvolvimento. Para mais informações
sobre os componentes do código confira o relatório do projeto.

"""
##

from socket import *
import threading

# Dicionário para armazenar os tópicos e seus assinantes
topicosAssinantes = {}

# Função para receber e processar mensagens de clientes
def handle_client(client):
    while True:
        data = client.recv(2038)
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

#Corpo do código do broker

# Definição do endereço IP e Porta para o programa broker
host = "0.0.0.0"
porta = "padrao definida pelo SO"

# Criação do objeto socket TCP mais explicado no relatório
server_socket = socket(AF_INET, SOCK_STREAM)

#Configurando porta 
server_socket.bind((host, 0))
server_socket.listen()

mensagem = "Servidor ouvindo: IP {} e porta {}"
print(mensagem.format(host, porta))

# Laço para que os clientes possam se conectar ao broker
while True:

    #Client = objeto socket para passar dados na comunicação cliente servidor
    #address = tupla contendo a informação Endereço IP e numero de porta de cliente
    client, address = server_socket.accept()

    mensagem = client.recv(2048).decode()
    #O objeto socket client irá receber uma sequência de até 2048 bytes que será decodificada pelo método

        # cria uma thread para os assinantes
    if mensagem.startswith("assinar"):
        threadAssinante = threading.Thread(target = subscribe, args = (client, address, mensagem))
        threadAssinante.start()

    # cria uma thread para publicar as mensagens
    elif mensagem.startswith("publicar"):
        threadPublicacao = threading.Thread(target = publish, args = (client, address, mensagem))
        threadPublicacao.start()

    # chama a função para listar os topicos e seus assinantes
    elif mensagem.startswith("list"):
        lista = list_topics(client)

    #threading.Thread(target=handle_client, args=(client,)).start()


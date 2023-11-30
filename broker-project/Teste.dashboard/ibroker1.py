import socket
import threading

# Lista para armazenar os clientes (sensores)
clients = []

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            # Encaminha a mensagem recebida para todos os clientes (dashboard)
            for dashboard_client in clients:
                dashboard_client.send(data)
        except Exception as e:
            print(f"Erro: {e}")
            break

def main():
    host = 'localhost'
    port = 5000

    broker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    broker_socket.bind((host, port))
    broker_socket.listen(5)

    print("Broker está ativo e aguardando conexões...")

    while True:
        client_socket, addr = broker_socket.accept()
        print(f"Conexão estabelecida com {addr}")
        
        # Adiciona o cliente à lista de clientes conectados (sensores)
        clients.append(client_socket)

        # Cria uma thread para lidar com as mensagens do cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()

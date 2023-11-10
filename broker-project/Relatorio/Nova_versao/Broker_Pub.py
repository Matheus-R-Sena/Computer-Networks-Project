import socket
import argparse

# Função para conectar ao servidor Broker
def conectar_ao_servidor(host, porta):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((host, porta))
        return cliente
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

# Função para publicar uma mensagem em um tópico
def publicar_mensagem(cliente, topico, mensagem):
    if cliente:
        try:
            # Monta o comando de publicação com o tópico e a mensagem
            comando = f"publish {topico} {mensagem}"
            cliente.send(comando.encode())
            
            # Recebe a confirmação do Broker
            confirmacao = cliente.recv(1024).decode()
            
            # Verifica se a publicação foi confirmada e imprime a mensagem
            if "publicação confirmada" in confirmacao:
                print(f"Publicação no tópico {topico} realizada: MENSAGEM:{mensagem}")
            else:
                print(f"Erro na publicação: {confirmacao}")
        except Exception as e:
            print(f"Erro na publicação: {e}")

def main():
    host = '127.0.0.1'
    porta = 8081  # Certifique-se de usar a porta correta

    parser = argparse.ArgumentParser(description="Cliente de Publicação no Broker")
    
    # Argumentos para especificar o tópico e a mensagem
    parser.add_argument("-t", help="Tópico", required=True)
    parser.add_argument("-m", help="Mensagem para publicação", required=True)
    args = parser.parse_args()
    topico = args.t
    mensagem = args.m

    cliente = conectar_ao_servidor(host, porta)
    if not cliente:
        return

    publicar_mensagem(cliente, topico, mensagem)
    
    # Encerra a conexão após a publicação
    cliente.close()

if __name__ == "__main__":
    main()

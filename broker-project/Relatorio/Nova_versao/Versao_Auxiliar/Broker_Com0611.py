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

# Função para enviar o comando "LIST" e receber uma resposta
def enviar_comando_list(cliente):
    if cliente:
        try:
            cliente.send("list".encode())
            resposta = cliente.recv(1024).decode()
            return resposta
        except Exception as e:
            print(f"Erro no envio do comando 'list': {e}")
    return ""

def main():
    host = '127.0.0.1'
    porta = 8081

    parser = argparse.ArgumentParser(description="Cliente de Comando para o Broker")
    parser.add_argument("-c", help="Comando", required=True)
    args = parser.parse_args()
    comando = args.c

    if comando == "list":
        cliente = conectar_ao_servidor(host, porta)
        if not cliente:
            return

        resposta = enviar_comando_list(cliente)

        if "COMANDO_CONFIRMATION_ACK" in resposta:
            print("Comando LIST confirmado pelo Broker.")
            dados_tabela = cliente.recv(1024).decode()
            print("Tabela de Tópicos e Assinantes:")
            print(dados_tabela)
        else:
            print(f"Erro no comando LIST: {resposta}")

        cliente.close()
    else:
        print(f"Comando '{comando}' não suportado.")

if __name__ == "__main__":
    main()
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

# Função para enviar o comando especificado e receber uma resposta
def enviar_comando(cliente, comando):
    if cliente:
        try:
            cliente.send(comando.encode())
            resposta = cliente.recv(1024).decode()
            return resposta
        except Exception as e:
            print(f"Erro no envio do comando '{comando}': {e}")
    return ""

def main():
    host = '127.0.0.1'
    porta = 8081

    parser = argparse.ArgumentParser(description="Cliente de Comando para o Broker")
    parser.add_argument("-c", help="Comando", required=True)
    args = parser.parse_args()
    comando = args.c

    cliente = conectar_ao_servidor(host, porta)
    if not cliente:
        return

    resposta = enviar_comando(cliente, comando)

    if "COMANDO_CONFIRMATION_ACK" in resposta:
        print(f"Comando {comando} confirmado pelo Broker.")
        if comando == "LIST":
            dados_tabela = cliente.recv(1024).decode()
            print("Tabela de Tópicos e Assinantes:")
            print(dados_tabela)
    else:
        print(f"Erro no comando {comando}: {resposta}")

    cliente.close()

if __name__ == "__main__":
    main()

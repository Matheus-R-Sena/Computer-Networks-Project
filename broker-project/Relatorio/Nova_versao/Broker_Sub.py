import socket
import argparse

def conectar_ao_servidor(host, porta):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((host, porta))
        return cliente
    except Exception as e:
        print(f"Erro na conexão: {e}")
        return None

def assinar_topicos(cliente, topicos):
    if cliente:
        try:
            comando = "subscribe " + " ".join(topicos)
            cliente.send(comando.encode())
            confirmacao = cliente.recv(1024).decode()
            print(f"Confirmação do servidor: {confirmacao}")
            return cliente, confirmacao
        except Exception as e:
            print(f"Erro na assinatura: {e}")
    return None, ""

def formatar_mensagem(mensagem):
    if ' ' in mensagem:
        topico, texto_mensagem = mensagem.split(maxsplit=1)
        print(f"TOPICO:{topico} MENSAGEM:{texto_mensagem}")
    else:
        print(f"Formato de mensagem inválido: {mensagem}")

def main():
    host = '127.0.0.1'
    porta = 8081  # Certificar de usar a porta correta

    parser = argparse.ArgumentParser(description="Cliente de Assinatura para o Broker")
    parser.add_argument("-t", nargs="+", help="Tópicos", required=True)
    entrada = parser.parse_args()
    topicos = entrada.t

    cliente = conectar_ao_servidor(host, porta)
    if not cliente:
        return

    cliente, confirmacao = assinar_topicos(cliente, topicos)

    if "assinatura confirmada" in confirmacao:
        print("Assinatura realizada!")

        while True:
            mensagem = cliente.recv(1024).decode()
            formatar_mensagem(mensagem)

    else:
        print("Erro ao assinar o tópico.")

if __name__ == "__main__":
    main()

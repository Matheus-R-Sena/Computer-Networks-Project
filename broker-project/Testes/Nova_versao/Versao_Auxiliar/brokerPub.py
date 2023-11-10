import socket       # biblioteca para estabelecer as conexões
import argparse     # biblioteca para configurar os argumentos da linha de comando

#função para publicar mensagem nos tópicos
def publicarMensagens(topico, mensagem):
    host = '127.0.0.1'   # endereço do servidor 
    porta = 8081        # porta do servidor

    try:
        # criação do socket TCP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # conexão com o servidor
        cliente.connect((host, porta))

        # envia a mensagem para publicada no tópico especificado
        comando = f"publish {topico} {mensagem}"
        cliente.send(comando.encode())

        # recebe uma mensagem de confirmação do servidor
        confirmacao = cliente.recv(1024).decode()

        # verifica a mensagem de confirmação 
        if confirmacao == "publicacao confirmada":

            # formatação da mensagem para a saida
            mensagemFormatada = str(mensagem)
            caracteres = "[',]"

            for c in caracteres:
                mensagemFormatada = mensagemFormatada.replace(c,'')

            print(f"Mensagem publicada no tópico {topico}: {mensagemFormatada}")

        else:
            print("Erro ao publicar mensagem no tópico")

    # exceções caso ocorra algo erro na conexão
    except Exception as e:
        print(f"Erro na conexão: {e}")

    # encerra a conexão com o servidor
    finally:
        cliente.close()


# configuração dos argumentos da linha de comando
argumentos = argparse.ArgumentParser(description = "modulo brokerPub")
argumentos.add_argument("-t", help = "tópico", required = True)
argumentos.add_argument("-m", nargs = "+", help = "mensagem", required = True)
entrada = argumentos.parse_args()
publicarMensagens(entrada.t, entrada.m)
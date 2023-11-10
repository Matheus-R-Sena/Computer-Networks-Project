import socket
import argparse

# Função para assinar tópicos já existentes ou criar novos tópicos
def assinarTopicos(topicos):
    host = '0.0.0.0'   # Endereço do servidor
    porta = 8000        # Porta do servidor

    try:
        # Criação do socket TCP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conexão com o servidor
        cliente.connect((host, porta))

        # Envia a solicitação para assinar os tópicos especificados
        comando = "subscribe " + " ".join(topicos)
        cliente.send(comando.encode())

        # Formatação dos tópicos para a saída
        topicosFormatados = " ".join(topicos)
        caracteres = "[']"

        for c in caracteres:
            topicosFormatados = topicosFormatados.replace(c, '')

        print(f"Assinando tópicos: {topicosFormatados}")

        # Recebe uma mensagem de confirmação do servidor
        confirmacao = cliente.recv(2048).decode()

        print(f"Confirmação do servidor: {confirmacao}")

        # Verifica a mensagem de confirmação
        if confirmacao == "subscription_confirmed":
            print("Assinatura realizada!")

            # Recebe e imprime as mensagens dos tópicos inscritos
            while True:
                mensagem = cliente.recv(2048).decode()

                # Formatação dos tópicos e das mensagens para a saída
                topico = mensagem.split()[0]
                frase = mensagem.split()[1:]
                fraseFormatada = ' '.join(frase)
                caracteres = "[',]"

                for c in caracteres:
                    fraseFormatada = fraseFormatada.replace(c, '')

                print(f"Tópico = {topico}    Mensagem = {fraseFormatada}")

        else:
            print("Erro ao assinar o tópico.")

    # Exceções caso ocorra algum erro na conexão
    except Exception as e:
        print(f"Erro na conexão: {e}")

# Configuração dos argumentos da linha de comando
argumentos = argparse.ArgumentParser(description="Cliente do Broker")
argumentos.add_argument("-t", nargs="+", help="Tópicos", required=True)
entrada = argumentos.parse_args()
assinarTopicos(entrada.t)


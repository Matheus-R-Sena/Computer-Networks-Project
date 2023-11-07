import socket

def publicarMensagens(topico, mensagem):
    # Configurações de conexão
    host = '0.0.0.0'  # Endereço do servidor
    porta = 8080      # Porta do servidor

    try:
        # Criação do socket TCP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conexão com o servidor
        cliente.connect((host, porta))

        # Monta o comando de publicação
        comando = f"publicar {topico} {mensagem}"
        
        # Envia o comando para o servidor
        cliente.send(comando.encode())

        # Recebe uma mensagem de confirmação do servidor
        confirmacao = cliente.recv(1024).decode()

        # Verifica se a publicação foi confirmada
        if confirmacao == "publicacao confirmada":
            # Formata a mensagem para a saída, removendo caracteres indesejados
            mensagemFormatada = ' '.join(mensagem)
            caracteres = "[',]"
            for c in caracteres:
                mensagemFormatada = mensagemFormatada.replace(c, '')

            # Imprime a mensagem publicada
            print(f"Mensagem publicada no tópico {topico}: {mensagemFormatada}")
        else:
            print("Erro ao publicar mensagem no tópico")

    # Tratamento de exceções em caso de erro de conexão
    except Exception as e:
        print(f"Erro na conexão: {e}")

    # Encerra a conexão com o servidor, independentemente de sucesso ou erro
    finally:
        cliente.close()

if __name__ == "__main__":
    # Solicita ao usuário que insira o tópico e a mensagem a serem publicados
    topico = input("Digite o tópico para publicar: ")
    mensagem = input("Digite a mensagem para publicar: ")
    
    # Chama a função publicarMensagens com os valores inseridos pelo usuário
    publicarMensagens(topico, mensagem)

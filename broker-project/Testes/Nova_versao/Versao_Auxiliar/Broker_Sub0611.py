import socket  # Importa o módulo 'socket' para comunicação por meio de sockets
import argparse  # Importa o módulo 'argparse' para analisar argumentos da linha de comando

# Função para conectar ao servidor
def conectar_ao_servidor(host, porta):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um objeto de socket TCP
        cliente.connect((host, porta))  # Conecta-se ao servidor especificado
        return cliente  # Retorna o objeto de socket do cliente
    except Exception as e:
        print(f"Erro na conexão: {e}")  # Imprime uma mensagem de erro, se a conexão falhar
        return None  # Retorna 'None' para indicar uma falha na conexão

# Função para assinar tópicos no servidor
def assinar_topicos(cliente, topicos):
    if cliente:
        try:
            # Construir o comando de assinatura concatenando os tópicos
            comando = "subscribe " + " ".join(topicos)
            cliente.send(comando.encode())  # Envia o comando de assinatura ao servidor
            confirmacao = cliente.recv(1024).decode()  # Recebe a confirmação do servidor
            print(f"Confirmação do servidor: {confirmacao}")  # Imprime a confirmação recebida
            return cliente, confirmacao  # Retorna o objeto de socket do cliente e a confirmação
        except Exception as e:
            print(f"Erro na assinatura: {e}")  # Imprime uma mensagem de erro, se a assinatura falhar
    return None, ""  # Retorna 'None' e uma string vazia para indicar uma falha na assinatura

# Função para formatar e imprimir mensagens recebidas
def formatar_mensagem(mensagem):
    if ' ' in mensagem:  # Verifica se a mensagem contém um espaço (indicando tópico e mensagem)
        topico, texto_mensagem = mensagem.split(maxsplit=1)  # Divide a mensagem em tópico e texto
        print(f"TOPICO:{topico} MENSAGEM:{texto_mensagem}")  # Imprime o tópico e a mensagem formatados
    else:
        print(f"Formato de mensagem inválido: {mensagem}")  # Imprime uma mensagem de erro se o formato da mensagem for inválido

# Função principal
def main():
    host = '127.0.0.1'  # Define o endereço IP do servidor
    porta = 8081  # Define o número da porta a ser usada (certifique-se de usar a porta correta)

    # Configurar um analisador de argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Cliente de Assinatura para o Broker")
    parser.add_argument("-t", nargs="+", help="Tópicos", required=True)  # Permite que o usuário especifique tópicos a serem assinados
    entrada = parser.parse_args()  # Analisa os argumentos da linha de comando
    topicos = entrada.t  # Armazena os tópicos especificados pelo usuário

    # Conectar ao servidor
    cliente = conectar_ao_servidor(host, porta)  # Chama a função para conectar ao servidor
    if not cliente:
        return  # Se a conexão falhar, encerra o programa

    # Assinar tópicos e receber a confirmação
    cliente, confirmacao = assinar_topicos(cliente, topicos)  # Chama a função para assinar tópicos

    if "assinatura confirmada" in confirmacao:
        print("Assinatura realizada!")  # Imprime uma mensagem de sucesso se a assinatura for confirmada

        # Aguardar e formatar mensagens continuamente
        while True:
            mensagem = cliente.recv(1024).decode()  # Recebe mensagens do servidor
            formatar_mensagem(mensagem)  # Chama a função para formatar e imprimir a mensagem

    else:
        print("Erro ao assinar o tópico.")  # Imprime uma mensagem de erro se a assinatura falhar

if __name__ == "__main__":
    main()  # Executa a função principal quando o arquivo é executado diretamente

import socket
import argparse

# Função para conectar ao servidor Broker
def conectar_ao_servidor(host, porta):
    try:
        # Cria um objeto de soquete usando a família de endereços IPv4 (AF_INET) e o tipo de soquete TCP (SOCK_STREAM)
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Tenta estabelecer uma conexão com o servidor Broker no host e porta especificados
        cliente.connect((host, porta))
        
        # Retorna o objeto de soquete se a conexão for bem-sucedida
        return cliente
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro e retorna None
        print(f"Erro na conexão: {e}")
        return None

# Função para publicar uma mensagem em um tópico
def publicar_mensagem(cliente, topico, mensagem):
    if cliente:
        try:
            # Monta o comando de publicação com o tópico e a mensagem
            comando = f"publish {topico} {mensagem}"
            
            # Envia o comando codificado para o servidor
            cliente.send(comando.encode())
            
            # Recebe a confirmação do Broker (servidor)
            confirmacao = cliente.recv(1024).decode()
            
            # Verifica se a publicação foi confirmada e imprime a mensagem apropriada
            if "publicação confirmada" in confirmacao:
                print(f"Publicação no tópico {topico} realizada: MENSAGEM:{mensagem}")
            else:
                print(f"Erro na publicação: {confirmacao}")
        except Exception as e:
            # Em caso de erro na publicação, imprime uma mensagem de erro
            print(f"Erro na publicação: {e}")

import socket
import argparse

# Função para conectar ao servidor Broker
def conectar_ao_servidor(host, porta):
    try:
        # Cria um objeto de soquete usando a família de endereços IPv4 (AF_INET) e o tipo de soquete TCP (SOCK_STREAM)
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Tenta estabelecer uma conexão com o servidor Broker no host e porta especificados
        cliente.connect((host, porta))
        
        # Retorna o objeto de soquete se a conexão for bem-sucedida
        return cliente
    except Exception as e:
        # Em caso de erro, imprime uma mensagem de erro e retorna None
        print(f"Erro na conexão: {e}")
        return None

# Função para publicar uma mensagem em um tópico
def publicar_mensagem(cliente, topico, mensagem):
    if cliente:
        try:
            # Monta o comando de publicação com o tópico e a mensagem
            comando = f"publish {topico} {mensagem}"
            
            # Envia o comando codificado para o servidor
            cliente.send(comando.encode())
            
            # Recebe a confirmação do Broker (servidor)
            confirmacao = cliente.recv(1024).decode()
            
            # Verifica se a publicação foi confirmada e imprime a mensagem apropriada
            if "publicação confirmada" in confirmacao:
                print(f"Publicação no tópico {topico} realizada: MENSAGEM:{mensagem}")
            else:
                print(f"Erro na publicação: {confirmacao}")
        except Exception as e:
            # Em caso de erro na publicação, imprime uma mensagem de erro
            print(f"Erro na publicação: {e}")

def main():
    host = '127.0.0.1'  # Endereço IP do servidor Broker
    porta = 8081       # Porta para se conectar ao servidor Broker (certifique-se de usar a porta correta)

    # Configuração do analisador de argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Cliente de Publicação no Broker")
    
    # Argumentos para especificar o tópico e a mensagem a serem publicados
    parser.add_argument("-t", help="Tópico", required=True)
    parser.add_argument("-m", help="Mensagem para publicação", required=True)
    args = parser.parse_args()
    topico = args.t
    mensagem = args.m

    # Tenta conectar ao servidor Broker
    cliente = conectar_ao_servidor(host, porta)
    if not cliente:
        return

    # Chama a função para publicar a mensagem no tópico
    publicar_mensagem(cliente, topico, mensagem)
    
    # Encerra a conexão após a publicação
    cliente.close()

if __name__ == "__main__":
    main()  # Chama a função principal se o script for executado como um programa principal

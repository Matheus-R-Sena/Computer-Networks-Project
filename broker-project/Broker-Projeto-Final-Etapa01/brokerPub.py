import socket
import argparse

def imprime_Mensagem_Topico(mensagem):
    """
    Método que imprime cada item da lista de strings. Por uma questão operacional vamos manter a mensagem como uma lista de strings, 
    sempre que quisermos imprimir de forma formatada usaremos o método imprime_Mensagem_Topico()
    """
    print("\n")
    for palavra in mensagem:
        print(palavra, end=' ')
    print("\n\n")


def Publica (topico, mensagem, cliente):

    # Colocando o marcador publicar para o broker 
    comando = f"publicar {topico} {mensagem}"

    print("\nPublicando tópico...\n")

    #envia comando com o marcador
    cliente.send(comando.encode())

    # recebe uma mensagem de confirmação do servidor
    confirmacao = cliente.recv(1024).decode()

    # verifica a mensagem de confirmação 
    if confirmacao == "publicacao confirmada":

        print(f"Tópico: \n\n{topico}")
        print(f"\nMensagem: ")
        imprime_Mensagem_Topico(mensagem)
        print("Publicação confirmada\n\n")

    else:
        print("falha ao publicar mensagem no tópico")


    # encerra a conexão com o servidor

    cliente.close()

#Estabelecimento da conexão

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Função usada para conectar ao servidor
cliente.connect(('127.0.0.1', 9000))


# configuração dos argumentos da linha de comando
argumentos = argparse.ArgumentParser(description = "modulo brokerPub")
argumentos.add_argument("-t", help = "tópico", required = True)
argumentos.add_argument("-m", nargs = '+', help = "mensagem", required = True)
entrada = argumentos.parse_args()

Publica(entrada.t, entrada.m, cliente)
"""
Entrada.t é uma string que representa o tópico e t é um atributo que aponta para a palavra referente ao tópico passado por linha de comando.

entrada.m referencia a mensagem que como irá receber muitos valores segundo especificado em nargs = '+', com isso os argumentos passados em linha
de comando irão compor uma lista de strings no formato:

[string 1, string 2 , string 3 , string 4 , string 5 , string 6 , string 7 , string 8 , string 9 , string 20 ,..... string n]

"""
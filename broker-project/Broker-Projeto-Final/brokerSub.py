import socket
import argparse

def assinar(topicos):

    # cria um objeto socket para o Sub
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 9000)) # conexão do cliente com o servidor
    #Utilizamos o comando connect do objeto cliente para fazer a conexão com o servidor a partir de seus endereços de IP e porta

    comando = f"assinar "  + " ".join(topicos)
    cliente.send(comando.encode()) # envia comando para broker
    print(comando) # imprime o comando
    
    confirmacao = cliente.recv(1024).decode() # recebe mensagem de confirmação do cliente


    if confirmacao == "assinatura confirmada":
        print("Assinatura realizada com sucesso")
        
        while True:
            
            dado = cliente.recv(1024).decode()   
            if(dado != "assinatura confirmada" and dado != "Assinatura realizada"):
                info = dado.split()
                mensagem = info[0]
                topico = info[1]      
                print(f"Mensagem: {mensagem} Topico: {topico}")
            else:
                print(dado)


# estrutura para envio de comando
parser = argparse.ArgumentParser(description="Broker Subscriber")
parser.add_argument("-t", nargs='+', required=True, help="Lista de topicos")
args = parser.parse_args()
assinar(args.t)


#Bibliotecas Utilizadas
import socket
import argparse

def assinar(cliente):

    #Adiciona "assinar" na lista de tópicos como flag para o broker
    comando = "assinar"
    
    #Enviando comando e tópicos para o broker
    cliente.send(comando.encode())
   
    
    #Recebe a mensagem de confirmação da assinatura nos tópicos
    confirmacao = cliente.recv(1024).decode() 
   

    if confirmacao == "assinatura confirmada":
        print("Assinatura realizada com sucesso nos tópicos:")
        for i in topicos:
            print(f"Topico assinado: {i}")
        
        
        while True:
            
            dado = cliente.recv(1024).decode()   
            if(dado != "assinatura confirmada"):
                topico, mensagem = dado[0], " ".join(dado[1:])
                     
                print(f"Mensagem: {mensagem} Topico: {topico}")
            else:
                print(dado)
    else:
        print("Falha na assinatura")



#Setup da conexão
try:

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # cria um objeto socket para o Sub
    cliente.connect(('127.0.0.1', 9000)) 
    #Utilizamos o comando connect do objeto socket "cliente" para fazer a conexão com o servidor a partir de seus endereços de IP e porta

    print("\nConexão estabelecida com o Servidor\n")

except Exception as e:
    print(f"Falha ao se conectar com o servidor {e} \n\n Por favor verifique o status do servidor")

    
# Comandos no Terminal

#Chamada do método assinar
assinar(cliente)


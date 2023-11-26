
#Bibliotecas Utilizadas
import socket
import argparse

def assinar(cliente):

    #Adiciona "assinar" na lista de tópicos como flag para o broker
    FLAG = "assinar"
    
    #Enviando comando e tópicos para o broker
    cliente.send(FLAG.encode())

    print("\nVocê não está assinando nenhum tópico\n")

    print("\nGostaria de se inscrever em um tópico?\n")
    
    print("\nSe sim, para mostrar os tópicos oferecidos pelo broker digite: topicos")
    print("\nSe não, para finalizar o programa digite sair:\n")
    print("\nObs: O cliente só poderá se inscrever em um tópico.\n")

    comando = input("Comando: ")

    if comando == "topicos":
        cliente.send("requisita".encode())

        


    elif comando == "sair":
        print("outra coisa")

    else:
        print("comando inválido, programa finalizado.")

    #conexão finalizada
    cliente.close()

   
    
    



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


import socket
import argparse

def envia_lista_comando_para_broker(comando): # função para enviar lista de tópicos e subscribers
   
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria um cliente de socket
        cliente.connect(("127.0.0.1", 8081)) # estabelece uma conexão TCP com servidor de endereço 127.0.0.1 na porta 8081
    

        if comando =="LIST":
            # Envia o comando "LIST" para o broker
            cliente.send("LIST".encode())

            confirmacao = cliente.recv(1024).decode() # recebe confirmação de envio
            print(f"Confirmação: {confirmacao}")  
            if confirmacao == "COMMAND_CONFIRMATION_ACK":
                print("Lista de tópicos e subscribers:")
                lista = cliente.recv(1024).decode()
                print(lista)  # imprime a lista mantida e enviada pelo broker

            cliente.close()  # fecha a conexão com o broker

    except Exception as e:
        print(f"Erro: {e}")

# estrutura para envio de comando
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description = "modulo brokerCom")
  parser.add_argument("-c", help = "comando", required = True)
  entrada = parser.parse_args()
  envia_lista_comando_para_broker(entrada.c)
    

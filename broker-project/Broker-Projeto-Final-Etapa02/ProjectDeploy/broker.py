import socket
import threading
import re
"""
Biblioteca utilizada pela função ClientePublica, para diferenciar os dados que estão chegando. Talvez de
vamos fazer isso no Subscriber.
"""

# Dicionário que armazena tópicos como chaves e seus respectivos assinantes
topicos_e_Assinantes = {} 
"""
Temos aqui um dicionário no modelo chave valor, que para uma chave temos n valores. Para a aplicação:
uma chave será o tópico e seus valores serão as refências dos objetos sockets clientes dos programas que assinaram aquele tópico
no seguinte formato:

DIC = {Clima: [cliente1, cliente2, cliente3], Temperatura: [cliente4, cliente5, cliente6]}

"""


#Função para a conexão
def comunicacao(servidor):
    try:
        while True:
            
            cliente, endereco = servidor.accept()  # aceita a conexão com o cliente

            
            mensagem = cliente.recv(1024).decode()  # recebe o comando do cliente

            # cria uma thread para os assinantes
            if mensagem.startswith("assinar"):
            
                threadAssinante = threading.Thread(target = clienteAssina, args = (cliente, endereco))
                
                threadAssinante.start()
                

            # cria uma thread para publicar as mensagens
            elif mensagem.startswith("publicar"):
                threadPublicacao = threading.Thread(target = clientePublica, args = (cliente, endereco, mensagem))
                threadPublicacao.start()
        

            # chama a função para listar os topicos e seus assinantes
            elif mensagem.startswith("list"):
                listarTopicosAssinantes(cliente)

    except Exception as e:
        print(f"Erro na conexão servidor: {e}") # exceção caso a conexão não seja feita





def clienteAssina (cliente, endereco): # função para adicionar um cliente à lista de assinantes de um tópico
    
    #Informa que tudo está Ok tanto no broker quanto no cliente
    print(f"\nConexão realizada com sucesso com o cliente no endereço (\"IP\", PORTA) {endereco}.", end="")
    
    #Recebendo requisição para assinar os tópicos
    comando = cliente.recv(1024).decode()
    if comando == "requisita":
        print("manda os tópicos")
    else:
        print("O cliente cancelou a conexão")
        cliente.close()








def clientePublica(cliente, endereco, mensagem): #Passamos o objeto socket cliente e a mensagem vinda dele.
    
    #Informa que tudo está Ok tanto no broker quanto no cliente
    print(f"\nConexão realizada com sucesso com o cliente no endereço (\"IP\", PORTA) {endereco}.", end="")
    topico = mensagem.split()[1]
    print(f" Tipo cliente: Simulador {topico}\n")

    #Adiciona a lista de Tópicos

    if topico not in topicos_e_Assinantes:
        topicos_e_Assinantes[topico] = []
        """estamos adicionando aqui um novo tópico"""

    #Envia mensagem para seus assinantes.
    
    while True:

        #Mensagem do Sensor sendo recebida
        msg = cliente.recv(1024).decode()
        print(msg)

        #Veremos se é uma String ou um número
        if (len(topicos_e_Assinantes[topico]) > 0):
            for Cliente_Socket in topicos_e_Assinantes[topico]:
                Cliente_Socket.sendall(msg.encode())
        else:
            print("Não temos assinantes no momento...")

        #Mandar para os assinantes


    
    
   

def listarTopicosAssinantes(cliente):
    # envia uma mensagem de confirmação para o cliente
    cliente.send("confirmado".encode())    
    
    dado = ""

    for topico, assinantes in topicos_e_Assinantes.items():
        Enderecos_Assinantes = [str(s.getpeername()) for s in assinantes]
        Assinantes_str = ', '.join(Enderecos_Assinantes)
        
        dado += f"{topico}: {Assinantes_str}\n"

    cliente.send(dado.encode())


#Programa Principal

# Servidor Setup
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("127.0.0.1", 9000))
servidor.listen()
print("Servidor escutando na porta 9000")

# Comunicação do Servidor
comunicacao(servidor)




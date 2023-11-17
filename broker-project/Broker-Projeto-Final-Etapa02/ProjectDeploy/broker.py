import socket
import threading

# Dicionário que armazena tópicos como chaves e seus respectivos assinantes
topicos_e_Assinantes = {} 


#Função para a conexão
def comunicacao(servidor):
    try:
        while True:

            cliente, endereco = servidor.accept()  # aceita a conexão com o cliente
    
            
            mensagem = cliente.recv(1024).decode()  # recebe o comando do cliente

            # cria uma thread para os assinantes
            if mensagem.startswith("assinar"):
            
                threadAssinante = threading.Thread(target = clienteAssina, args = (cliente, endereco, mensagem))
                
                threadAssinante.start()
                

            # cria uma thread para publicar as mensagens
            elif mensagem.startswith("publicar"):
                threadPublicacao = threading.Thread(target = clientePublica, args = (cliente,))
                threadPublicacao.start()
        

            # chama a função para listar os topicos e seus assinantes
            elif mensagem.startswith("list"):
                listarTopicosAssinantes(cliente)

    except Exception as e:
        print(f"Erro na conexão servidor: {e}") # exceção caso a conexão não seja feita





def clienteAssina (cliente, endereco, mensagem): # função para adicionar um cliente à lista de assinantes de um tópico
    try:

        
        topicos = mensagem.split()[1:]
    
        #Cliente
        for topico in topicos:
            if topico not in topicos_e_Assinantes:
                topicos_e_Assinantes[topico] = []
            topicos_e_Assinantes[topico].append(cliente)


        # envia uma mensagem de confirmação para o cliente
        cliente.send("assinatura confirmada".encode()) 

        print(f"Mensagem de confirmação enviada para cliente que requisitou o servico")

    # exceções caso ocorra algo erro na conexão
    except Exception as e:
        print(f"Erro na conexão com {endereco}: {e}")






def clientePublica(cliente): #Passamos o objeto socket cliente e a mensagem vinda dele.
   
    print("Conexão realizada com sucesso")
    while True:

        msg = cliente.recv(1024).decode()
        print(msg)





        """
        if topico in topicos_e_Assinantes: 

            cliente.send("publicacao confirmada".encode())
            for subscriber_socket in topicos_e_Assinantes[topico]: # percorre a lista de assinantes do topico
                
                print(f"MENSAGEM: {conteudo} TOPICO: {topico}")
                dado = topico +" "+ conteudo 

                subscriber_socket.sendall(dado.encode()) # envia a mensagem aos assinantes
                print(f"Mensagem enviada aos assinantes do topico:  {topico}") # imprime uma mensagem de confirmação de envio
                    
        else: # caso o topico não exista, envia uma mensagem que a publicaçao nao foi feita
            cliente.send("Publicacao nao confirmada".encode())
            print(f"Mensagem não enviada aos assinantes")  
        """
    
   

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




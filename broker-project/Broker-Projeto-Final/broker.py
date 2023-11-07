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
                threadPublicacao = threading.Thread(target = clientePublica, args = (cliente, mensagem))
                threadPublicacao.start()

            # chama a função para listar os topicos e seus assinantes
            elif mensagem.startswith("list"):
                listarTopicosAssinantes(cliente)

    except Exception as e:
        print(f"Erro na conexão servidor: {e}") # exceção caso a conexão não seja feita





def clienteAssina (cliente, endereco, mensagem): # função para adicionar um cliente à lista de assinantes de um tópico
    try:

        # Aqui, a variável topicos é criada dividindo a mensagem recebida em palavras e atribuindo à topicos todas as palavras a partir do segundo elemento (índice 1) 
        # em diante. Isso presumivelmente coleta uma lista de tópicos.
        topicos = mensagem.split()[1:]
        

        #Este trecho de código é um loop for que percorre cada elemento na lista topicos. Para cada elemento topico na lista topicos, 
        # o código verifica se topico não está no dicionário topicos_e_Assinantes. Se topico não estiver no dicionário,
        # o código adiciona uma nova chave topico ao dicionário com uma lista vazia como valor. 
        # Em seguida, o código adiciona o cliente à lista de assinantes do tópico.
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






def clientePublica(cliente, mensagem): #Passamos o objeto socket cliente e a mensagem vinda dele.
   
    #Extrai o nome do tópico e a mensagem a ser publicada da mensagem recebida do cliente.
    # A função split() é usada para dividir a mensagem em uma lista de palavras. A primeira palavra na lista é o comando “PUBLISH”, que não é 
    #   necessária para esta linha de código. A segunda palavra na lista é o nome do tópico, que é armazenado na variável topico. A mensagem a ser 
    #   publicada começa na terceira palavra da lista. Para extrair a mensagem, a função split() é usada novamente para dividir a lista de palavras
    #   a partir da terceira palavra em diante. Em seguida, a função join() é usada para 
    #   unir as palavras da lista em uma única string, separando cada palavra com um espaço. A mensagem resultante é armazenada na variável
    topico, conteudo = mensagem.split()[1], " ".join(mensagem.split()[2:]) 
                
    if topico in topicos_e_Assinantes: 

        cliente.send("publicacao confirmada".encode())
        for subscriber_socket in topicos_e_Assinantes[topico]: # percorre a lista de assinantes do topico
            
            print(f"MENSAGEM: {conteudo} TOPICO: {topico}")
            dado = conteudo + " " + topico  
            
            subscriber_socket.sendall(dado.encode()) # envia a mensagem aos assinantes
            print(f"Mensagem enviada aos assinantes do topico:  {topico}") # imprime uma mensagem de confirmação de envio
                
    else: # caso o topico não exista, envia uma mensagem que a publicaçao nao foi feita
        cliente.send("Publicacao nao confirmada".encode())
        print(f"Mensagem não enviada aos assinantes")  



def listarTopicosAssinantes(cliente):
    # envia uma mensagem de confirmação para o cliente
    cliente.send("confirmado".encode())    
    
    dado = ""

    #A variável dado é inicializada como uma string vazia. 
    
    
    # Em seguida, um loop for é usado para percorrer cada tópico e sua lista de assinantes no dicionário topicos_e_Assinantes. 
    # Para cada tópico, a função cria uma lista de endereços de assinantes usando a função getpeername() para obter o endereço de cada socket de assinante. 
    
    # Para o dicionário existente estamos rodando topico (chave) e assinantes (tupla correspondente a chave)
    #O método items() é usado para retornar uma lista de tuplas que contém o par chave-valor para cada item no dicionário. 
    #Cada tupla contém o nome do tópico como a chave e a lista de assinantes como o valor.
    for topico, assinantes in topicos_e_Assinantes.items():
        Enderecos_Assinantes = [str(s.getpeername()) for s in assinantes]
        Assinantes_str = ', '.join(Enderecos_Assinantes)
        # Em seguida, a lista de endereços é convertida em uma string separada por vírgulas usando a função join(). 
        # A string resultante é adicionada à variável dado com o nome do tópico.
        dado += f"{topico}: {Assinantes_str}\n"

    cliente.send(dado.encode())


#Programa Principal

# Servidor Setup
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("127.0.0.1", 8889))
servidor.listen()
print("Servidor escutando na porta 8888")

# Comunicação do Servidor
comunicacao(servidor)




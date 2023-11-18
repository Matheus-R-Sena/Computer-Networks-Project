
#Bibliotecas Utilizadas
import socket
import argparse

def assinar(topicos, cliente):

    #Adiciona "assinar" na lista de tópicos como flag para o broker
    comando = "assinar "+" ".join(topicos)
    """
    Aqui pegamos a lista de tópicos que foi passada para a variável tópicos e usamos o método join. O método join() é usado para concatenar 
    os elementos da lista de tópicos em uma única string, separando cada elemento com um espaço. A string resultante é então concatenada com 
    a palavra “assinar” usando o operador +.

    Se colocassemos somente "assinar".join(topicos), seria criada uma string onde cada elemento da lista de topicos seria separado pela string
    "assinar", lembre-se, join é um método de strig, com isso estamos aplicando esse método à um espaço vazio " ", dessa forma dizemos que cada
    elemento da lista será separado por um espaço vazio.

    Logo em seguida concatenamos à string "assinar". "assinar" não é controlada pelo usuário
    """
    
    #Enviando comando e tópicos para o broker
    cliente.send(comando.encode())
    """
    Enviando a string com o comando "assinar" capitaneando a string com os tópicos que esta aplicação cliente deseja assinar. Com o intuito de 
    encontrar a função apropriada para essa aplicação.
    """
    
    #Recebe a mensagem de confirmação da assinatura nos tópicos
    confirmacao = cliente.recv(1024).decode() 
    """
    Recebendo uma String de confirmação
    """

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

#Criação de uma interface para comandos no terminal
parser = argparse.ArgumentParser(description="Broker Subscriber")
"""
Cria um objeto da classe ArgumentParser que será apontado pela referência "parser". Este objeto le é responsável por definir e 
gerenciar os argumentos da linha de comando. Ele não lê diretamente do terminal, mas configura como os argumentos 
devem ser interpretados.
"""

#Configurando como os comandos devem ser escritos
parser.add_argument("-t", nargs='+', required=True, help="Lista de topicos")
"""
Utilizando método add_argument() do objeto "parser" criado, nós especificamos como o comando no terminal deve ser escrito.
O comando é escrito logo na inicialização do arquivo. 

No método especificamos que:

required=True : Argumentos obrigatórios, False para não obrigatórios

-t : É uma flag curta que é usada para identificar os argumentos que serão passados nessa linha de comando, normalmente flags
curtas são precedidas por um hífen, enquanto uma flag longa é precedida por 2, poderiamos trocar esse -t por --topico

nargs='+': número de argumentos maior que 1, se não colocássemos esse parâmetro a sobrecarga iria priorizar o método que obrigava
a colocar apenas um argumento e não N como é o caso, aqui podemos colocar de 1 (por conta de required true) a N argumentos.
"""
#Levando a Lista de argumentos  para um novo objeto recém criado args, referenciado por "argumentos"
argumentos = parser.parse_args()
"""
Esta linha é a que de fato lê as informações do Terminal.
O objeto args é retornado pelo método parse_args() aplicado ao objeto ArgumentParser criado anteriormente. Esse método retornará um objeto
args que irá armazenar os argumentos passados em uma lista de Strings, que será referênciada pelas flags passadas no método 
parser.add_argument("-t", nargs='+', required=True, help="Lista de topicos"). 

Depois disso poderemos acessar essa lista com argumentos.t, que é a flag que localiza essa lista no objeto.
"""
#Chamada do método assinar
assinar(argumentos.t, cliente)
"""Aqui passamos a lista de argumentos mais a referência do objeto socket "Cliente para a função assinar
"""

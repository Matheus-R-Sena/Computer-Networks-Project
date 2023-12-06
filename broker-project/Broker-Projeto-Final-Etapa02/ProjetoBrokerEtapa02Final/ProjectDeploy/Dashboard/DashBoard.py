#Dashboard apenas com a parte lógica pronta
# Comando para rodar o dashboard no navegador: 

# streamlit run .\DashBoard.py

import socket             
import threading          
import time               
import streamlit as st    

# lista de variável global com os valores dos topicos
topicos = [0, 0, 0]
contador_lock = threading.Lock()

# funcao para assinar os topicos
def comunicacao(servidor):
    try:
        contador = 0
        while True:
            
            # Confirmação de que os 3 subs estão conectados
            with contador_lock:
                if contador == 4:
                    break

            cliente, endereco = servidor.accept()  # aceita a conexão com o cliente 
            mensagem = cliente.recv(1024).decode()  # recebe o comando do cliente

            # cria uma thread para os assinantes
            if mensagem.startswith("Clima"):
                with contador_lock:
                    contador += 1
                threadClima = threading.Thread(target = AtualizaClima, args = (cliente,))
                threadClima.start()
 
            # cria uma thread para publicar as mensagens
            elif mensagem.startswith("Temperatura"):
                with contador_lock:
                    contador += 1
                threadTemperatura = threading.Thread(target = AtualizaTemperatura, args = (cliente,))
                threadTemperatura.start()
        

            # chama a função para listar os topicos e seus assinantes
            elif mensagem.startswith("Umidade"):
                with contador_lock:
                    contador += 1
                threadUmidade = threading.Thread(target = AtualizaUmidade, args = (cliente,))
                threadUmidade.start()

    except Exception as e:
        print(f"Erro na conexão servidor: {e}") # exceção caso a conexão não seja feita


def AtualizaClima (cliente):

    while True:
        #for topico in topicos:
            #if topico == "Clima":
            mensagem = cliente.recv(1024).decode()
            #Pegando IP e porta do broker
            Cliente_end, Cliente_porta = cliente.getpeername()
            print(f'Recebendo dado: {mensagem} do Subscriber 1 IP {Cliente_end} e porta {Cliente_porta}')

            if mensagem == "nublado":
                topicos[0] = 1
            elif mensagem == "ensolarado":
                topicos[0] = 2
            elif mensagem == "chuvoso":
                topicos[0] = 3
            


def AtualizaTemperatura (cliente):

    while True:
    #for topico in topicos:
        #if topico == "Temperatura":
        mensagem = cliente.recv(1024).decode()
        #Pegando IP e porta do broker
        Cliente_end, Cliente_porta = cliente.getpeername()
        print(f'Recebendo dado: {mensagem} do Subscriber 2 IP {Cliente_end} e porta {Cliente_porta}')
        topicos[1] = mensagem
        

def AtualizaUmidade (cliente):
    print("\n\n\n\n\n\n\n\n\nEstou na Umidade\n\n\n\n\n\n")
    while True:
        print("Estou na Umidade")
    
        #if topico == "Umidade":
        mensagem = cliente.recv(1024).decode()
        #print(mensagem)
        
        #Pegando IP e porta do broker
        Cliente_end, Cliente_porta = cliente.getpeername()
        print(f'Recebendo dado: {mensagem} do Subscriber 3 IP {Cliente_end} e porta {Cliente_porta}')
        topicos[2] = mensagem



def EstadoClima (Clima):

    if Clima == 1:
        palavraClima.markdown(f'<p style="color: orange; font-size: 4em; text-align: center;"> nublado </p>', unsafe_allow_html=True)

    elif Clima == 2:
        palavraClima.markdown(f'<p style="color: orange; font-size: 4em; text-align: center;"> ensolarado </p>', unsafe_allow_html=True)

    elif Clima == 3:
        palavraClima.markdown(f'<p style="color: orange; font-size: 4em; text-align: center;"> chuvoso </p>', unsafe_allow_html=True)

   


# funcoes para mudar as frases dos topicos
def EstadoTemperatura (temperatura):

    #Para transformar string em um número
    try:
        temperatura = float(temperatura)
    except ValueError:
        # Se a conversão falhar, defina a temperatura como 0 ou outro valor padrão
        temperatura = 0


    
    fraseTemperatura.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> Em graus celsius </p>', unsafe_allow_html=True)

    

# Dashboard

# Definindo o estilo do fundo
st.markdown(
    """
    <style>
        body {
            background-color: #ffffff; /* Cor branca */
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Dashboard Clima, temperatura e Umidade") 
st.write("\n") 

# Clima
st.markdown('<p style="color: yellow; font-size: 5em;"> Clima </p>', unsafe_allow_html=True)  # titulo do topico 1
 
st.write("\n")  

palavraClima = st.markdown('')  

st.write("\n")  
st.write("\n")  
st.write("\n") 

# Temperatura
st.markdown('<p style="color: red; font-size: 5em;"> Temperatura </p>', unsafe_allow_html=True)  # titulo do topico 2
st.text("0                                                                               60")  # faixa de variacao do topico 2
linha1 = st.progress(0) 
numero1 = st.markdown('')  

fraseTemperatura = st.markdown('')  # 

st.write("\n")  
st.write("\n")  
st.write("\n") 

st.write("\n") 

# Clima
st.markdown('<p style="color: blue; font-size: 5em;"> Umidade</p>', unsafe_allow_html=True)  
st.text("0                                                                               100")  
linha2 = st.progress(0)  
numero2 = st.markdown('')  

st.write("\n")  
st.write("\n")  
st.write("\n") 

# Setup Servidor Dashboard
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("127.0.0.1", 10000))
servidor.listen()
print("Servidor escutando na porta 15000")

comunicacao(servidor)

# Atualizar o dashboard
while True:

    # atualiza topicos
    v1 = float(topicos[0])
    v2 = float(topicos[1])
    v3 = float(topicos[2])

    
    linha1.progress(v2 / 100.0)
    linha2.progress(v3 / 100.0)

   
    numero1.markdown(f'<p style="color: red; font-size: 3em; text-align: center;"> {str(topicos[1])} </p>', unsafe_allow_html=True)
    numero2.markdown(f'<p style="color: lightblue; font-size: 3em; text-align: center;"> {str(topicos[2])} </p>', unsafe_allow_html=True)


    EstadoClima (topicos[0])
    fraseTemperatura.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> Em graus celsius </p>', unsafe_allow_html=True)
    
    time.sleep(2)
   
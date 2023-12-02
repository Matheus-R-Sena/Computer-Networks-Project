#Dashboard apenas com a parte lógica pronta
# Comando para rodar o dashboard no navegador: 
# streamlit run .\DashBoard.py

import socket             # biblioteca para estabelecer as conexões
import threading          # biblioteca para criar as threads
import time               # biblioteca para usar um tempo de espera
import streamlit as st    # biblioteca para criar o dashboard web

# lista com os topicos
topicos = ["Clima", "Temperatura", "Umidade"]

# lista com os valores dos topicos
variacoes = [0, 0, 0]

# funcao para assinar os topicos
def comunicacao(servidor):
    try:
        contador = 0
        while True:
            
            #Confirmação de que os 3 subs estão conectados
            if contador == 3:
                break

            cliente, endereco = servidor.accept()  # aceita a conexão com o cliente 
            mensagem = cliente.recv(1024).decode()  # recebe o comando do cliente

            # cria uma thread para os assinantes
            if mensagem.startswith("Clima"):
                contador = contador + 1
                threadClima = threading.Thread(target = AtualizaClima, args = (cliente,))
                threadClima.start()
 
            # cria uma thread para publicar as mensagens
            elif mensagem.startswith("Temperatura"):
                contador = contador + 1
                threadTemperatura = threading.Thread(target = AtualizaTemperatura, args = (cliente,))
                threadTemperatura.start()
        

            # chama a função para listar os topicos e seus assinantes
            elif mensagem.startswith("Umidade"):
                contador = contador + 1
                threadUmidade = threading.Thread(target = AtualizaUmidade, args = (cliente,))
                threadUmidade.start()

    except Exception as e:
        print(f"Erro na conexão servidor: {e}") # exceção caso a conexão não seja feita


def AtualizaClima (cliente):

    while True:
        #for topico in topicos:
            #if topico == "Clima":
            mensagem = cliente.recv(1024).decode()
            #print(mensagem)
            print(mensagem)

            if mensagem == "nublado":
                variacoes[0] = 1
            elif mensagem == "ensolarado":
                variacoes[0] = 2
            elif mensagem == "chuvoso":
                variacoes[0] = 3
            


def AtualizaTemperatura (cliente):

    while True:
    #for topico in topicos:
        #if topico == "Temperatura":
        mensagem = cliente.recv(1024).decode()
        #print(mensagem)
        variacoes[1] = mensagem
        print(variacoes[1])

def AtualizaUmidade (cliente):
    
    while True:

    #for topico in topicos:
        #if topico == "Umidade":
        mensagem = cliente.recv(1024).decode()
        #print(mensagem)
        variacoes[2] = mensagem
        print(variacoes[2])



def frasesClima (Clima):

    if Clima == 1:
        fraseClima.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> nublado </p>', unsafe_allow_html=True)

    elif Clima == 2:
        fraseClima.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> ensolarado </p>', unsafe_allow_html=True)

    elif Clima == 3:
        fraseClima.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> chuvoso </p>', unsafe_allow_html=True)

   


# funcoes para mudar as frases dos topicos
def frasesTemperatura (temperatura):

    #Para transformar string em um número
    try:
        temperatura = float(temperatura)
    except ValueError:
        # Se a conversão falhar, defina a temperatura como 0 ou outro valor padrão
        temperatura = 0


    if temperatura <= 20:
        fraseTemperatura.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> Está frio, coloca uma meia. Ass: Mãe </p>', unsafe_allow_html=True)

    elif 20 < temperatura <= 30:
        fraseTemperatura.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> Tempinho bom! </p>', unsafe_allow_html=True)

    elif 30 < temperatura <= 40:
        fraseTemperatura.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> Já dá para ligar o ar condicionado. </p>', unsafe_allow_html=True)

    elif 40 < temperatura <= 50:
        fraseTemperatura.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> Olha o aquecimento global como vai. </p>', unsafe_allow_html=True)

    elif 50 < temperatura <= 70:
        fraseTemperatura.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> Impossível sobreviver fora do freezer. </p>', unsafe_allow_html=True)

    else:
        fraseTemperatura.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> Já fomos com Deus. </p>', unsafe_allow_html=True)


def frasesUmidade (Umidade):

    #Para transformar string em um número
    try:
        Umidade = float(Umidade)
    except ValueError:
        # Se a conversão falhar, defina a temperatura como 0 ou outro valor padrão
        Umidade = 0

    if Umidade <= 25:
        fraseUmidade.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Céu limpo, tem chuva não. </p>', unsafe_allow_html=True)

    elif 25 < Umidade <= 40:
        fraseUmidade.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Coloca um guarda chuva na bolsa por precaução. </p>', unsafe_allow_html=True)

    elif 40 < Umidade <= 50:
        fraseUmidade.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Talvez venha chuva por aí. </p>', unsafe_allow_html=True)

    elif 50 < Umidade <= 60:
        fraseUmidade.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Será que vale a pena sair de casa hoje? </p>', unsafe_allow_html=True)

    elif 60 < Umidade <= 80:
       fraseUmidade.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Melhor já tirar as roupas do varal. </p>', unsafe_allow_html=True)

    else:
        fraseUmidade.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Se você sair de casa vai chover, acredite. </p>', unsafe_allow_html=True)


# formatacoes do dashboard
st.title("Dashboard Sensores") # titulo do dashboard
st.write("\n") # espaço em branco

# topico 1
st.markdown('<p style="color: orange; font-size: 2em;"> Clima </p>', unsafe_allow_html=True)  # titulo do topico 1
 

#linha1 = st.progress(0)  # cria a linha 1
#numero1 = st.markdown('')  # valor atual do topico

st.write("\n")  # espaço em branco

fraseClima = st.markdown('')  # frase atual do topico

st.write("\n")  # espaço em branco
st.write("\n")  # espaço em branco
st.write("\n") # espaço em branco

# topico 2
st.markdown('<p style="color: lightgreen; font-size: 2em;"> Temperatura </p>', unsafe_allow_html=True)  # titulo do topico 2
st.text("0                                                                               100")  # faixa de variacao do topico 2
linha2 = st.progress(0)  # cria a linha 2
numero2 = st.markdown('')  # valor atual do topico 

fraseTemperatura = st.markdown('')  # frase atual do topico

st.write("\n")  # espaço em branco
st.write("\n")  # espaço em branco
st.write("\n") # espaço em branco

st.write("\n")  # espaço em branco

# topico 3
st.markdown('<p style="color: lightblue; font-size: 2em;"> Umidade</p>', unsafe_allow_html=True)  # titulo do topico 3
st.text("0                                                                               100")  # faixa de variacao do topico 3
linha3 = st.progress(0)  # cria linha 3
numero3 = st.markdown('')  # valor atual do topico

st.write("\n") # espaço em branco

fraseUmidade = st.markdown('')  # frase atual do topico

st.write("\n")  # espaço em branco
st.write("\n")  # espaço em branco
st.write("\n") # espaço em branco


# for para criar as threads de assinantes
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("127.0.0.1", 10000))
servidor.listen()
print("Servidor escutando na porta 15000")

comunicacao(servidor)

#Checar


# loop para atualizar o dashboard
while True:

    # atualiza as linhas de cada topico
    v1 = float(variacoes[0])
    v2 = float(variacoes[1])
    v3 = float(variacoes[2])

    #linha1.progress(v1 / 100.0)
    linha2.progress(v2 / 100.0)
    linha3.progress(v3 / 100.0)

    # atualiza os valores de cada topico

    #numero1.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> {str(variacoes[0])} </p>', unsafe_allow_html=True)
    numero2.markdown(f'<p style="color: lightgreen; font-size: 1.8em; text-align: center;"> {str(variacoes[1])} </p>', unsafe_allow_html=True)
    numero3.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> {str(variacoes[2])} </p>', unsafe_allow_html=True)

    # atualiza as frases de cada topico
    frasesTemperatura (variacoes[0])
    frasesTemperatura(variacoes[1])
    frasesUmidade(variacoes[2])
    
    time.sleep(2)
   
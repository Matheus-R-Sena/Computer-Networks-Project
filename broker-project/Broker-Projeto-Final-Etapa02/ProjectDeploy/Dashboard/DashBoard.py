import socket             # biblioteca para estabelecer as conexões
import threading          # biblioteca para criar as threads
import time               # biblioteca para usar um tempo de espera
import streamlit as st    # biblioteca para criar o dashboard web

# lista com os topicos
topicos = ["temperatura", "vento", "chuva"]

# lista com os valores dos topicos
variacoes = [0, 0, 0]

# funcao para assinar os topicos
def assinarTopico(topico, posicao):
    host = "127.0.0.1"   # endereço do servidor 
    porta = 12450        # porta do servidor

    try:

        # criação do socket TCP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # conexão com o servidor
        cliente.connect((host, porta))

        # envia o comando para o broker
        comando = "assinar " + " ".join(topico)
        cliente.send(comando.encode())

        # recebe uma mensagem de confirmação do servidor
        confirmacao = cliente.recv(1024).decode()

        # verifica a mensagem de confirmação 
        if confirmacao == "assinatura confirmada":
            print("Assinatura realizada!")

            # loop para receber os dados
            while True:
                mensagem = cliente.recv(1024).decode()

                # verifica se a mensagem nao esta vazia
                if mensagem != '':

                    # atualiza a lista com os novos valores
                    variacoes[posicao] = float(mensagem) 

        else:
            print("Erro ao assinar o tópico.")

    # exceções caso ocorra algum erro na conexão
    except Exception as e:
        print(f"Erro na conexão: {e}")

# funcoes para mudar as frases dos topicos
def frasesTemperatura (temperatura):

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

def frasesVento (vento):

    if vento <= 20:
        fraseVento.markdown(f'<p style="color: lightgreen; font-size: 1.8em; text-align: center;"> Ventinho agradável. </p>', unsafe_allow_html=True)

    elif 20 < vento <= 30:
        fraseVento.markdown(f'<p style="color: lightgreen; font-size: 1.8em; text-align: center;"> Segura os papéis senão voa tudo. </p>', unsafe_allow_html=True)

    elif 30 < vento <= 40:
        fraseVento.markdown(f'<p style="color: lightgreen; font-size: 1.8em; text-align: center;"> Cheio de folhas no chão, olha lá. </p>', unsafe_allow_html=True)

    elif 40 < vento <= 50:
        fraseVento.markdown(f'<p style="color: lightgreen; font-size: 1.8em; text-align: center;"> Melhor ficar em casa mesmo. </p>', unsafe_allow_html=True)

    elif 50 < vento <= 70:
       fraseVento.markdown(f'<p style="color: lightgreen; font-size: 1.8em; text-align: center;"> Pelo amor de Deus não sai de casa! </p>', unsafe_allow_html=True)

    else:
        fraseVento.markdown(f'<p style="color: lightgreen; font-size: 1.8em; text-align: center;"> O telhado foi de arrasta para cima. </p>', unsafe_allow_html=True)

def frasesChuva (chuva):

    if chuva <= 25:
        fraseChuva.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Céu limpo, tem chuva não. </p>', unsafe_allow_html=True)

    elif 25 < chuva <= 40:
        fraseChuva.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Coloca um guarda chuva na bolsa por precaução. </p>', unsafe_allow_html=True)

    elif 40 < chuva <= 50:
        fraseChuva.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Talvez venha chuva por aí. </p>', unsafe_allow_html=True)

    elif 50 < chuva <= 60:
        fraseChuva.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Será que vale a pena sair de casa hoje? </p>', unsafe_allow_html=True)

    elif 60 < chuva <= 80:
       fraseChuva.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Melhor já tirar as roupas do varal. </p>', unsafe_allow_html=True)

    else:
        fraseChuva.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> Se você sair de casa vai chover, acredite. </p>', unsafe_allow_html=True)


# formatacoes do dashboard
st.title("Dashboard Sensores") # titulo do dashboard
st.write("\n") # espaço em branco

# topico 1
st.markdown('<p style="color: orange; font-size: 2em;"> Temperatura</p>', unsafe_allow_html=True)  # titulo do topico 1
st.text("0                                                                               100")   # faixa de variacao do topico 1
linha1 = st.progress(0)  # cria a linha 1
numero1 = st.markdown('')  # valor atual do topico

st.write("\n")  # espaço em branco

fraseTemperatura = st.markdown('')  # frase atual do topico

st.write("\n")  # espaço em branco
st.write("\n")  # espaço em branco
st.write("\n") # espaço em branco

# topico 2
st.markdown('<p style="color: lightgreen; font-size: 2em;"> Vento </p>', unsafe_allow_html=True)  # titulo do topico 2
st.text("0                                                                               100")  # faixa de variacao do topico 2
linha2 = st.progress(0)  # cria a linha 2
numero2 = st.markdown('')  # valor atual do topico 

st.write("\n")  # espaço em branco

fraseVento = st.markdown('')  # frase atual do topico

st.write("\n")  # espaço em branco
st.write("\n")  # espaço em branco
st.write("\n") # espaço em branco

# topico 3
st.markdown('<p style="color: lightblue; font-size: 2em;"> Chuva</p>', unsafe_allow_html=True)  # titulo do topico 3
st.text("0                                                                               100")  # faixa de variacao do topico 3
linha3 = st.progress(0)  # cria linha 3
numero3 = st.markdown('')  # valor atual do topico

st.write("\n") # espaço em branco

fraseChuva = st.markdown('')  # frase atual do topico


# for para criar as threads de assinantes
for topico in topicos:
    threadAssinante = threading.Thread(target = assinarTopico, args = (topico, topicos.index(topico)))
    threadAssinante.start()


# loop para atualizar o dashboard
while True:

    # atualiza as linhas de cada topico
    linha1.progress(variacoes[0] / 100.0)   
    linha2.progress(variacoes[1] / 100.0)
    linha3.progress(variacoes[2] / 100.0)

    # atualiza os valores de cada topico
    numero1.markdown(f'<p style="color: orange; font-size: 1.8em; text-align: center;"> {str(variacoes[0])} </p>', unsafe_allow_html=True)
    numero2.markdown(f'<p style="color: lightgreen; font-size: 1.8em; text-align: center;"> {str(variacoes[1])} </p>', unsafe_allow_html=True)
    numero3.markdown(f'<p style="color: lightblue; font-size: 1.8em; text-align: center;"> {str(variacoes[2])} </p>', unsafe_allow_html=True)

    # atualiza as frases de cada topico
    frasesTemperatura(variacoes[0])
    frasesVento(variacoes[1])
    frasesChuva(variacoes[2])
    
    time.sleep(1)
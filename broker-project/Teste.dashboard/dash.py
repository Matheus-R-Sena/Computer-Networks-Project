import socket
import streamlit as st
import threading

# Variáveis globais
temperature, wind_speed, rain_intensity = 0.0, 0.0, 0.0
update_event = threading.Event()

# Função para atualizar variáveis globais
def update_variables(data):
    global temperature, wind_speed, rain_intensity
    temperature, wind_speed, rain_intensity = map(float, data.split(','))
    update_event.set()

# Função para receber dados contínuos do servidor
def receive_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        update_variables(data.decode())

# Função para criar o dashboard usando Streamlit
def streamlit_dashboard():
    st.title("Condições Climáticas Simuladas")

    while True:
        update_event.wait()  # Aguarda até que o evento de atualização seja sinalizado
        st.text(f"Temperatura Atual: {temperature}°C")
        st.text(f"Velocidade do Vento Atual: {wind_speed} m/s")
        st.text(f"Intensidade da Chuva Atual: {rain_intensity}")

        # Adicione mais elementos do Streamlit conforme necessário

        update_event.clear()  # Limpa o evento para aguardar a próxima atualização

# Configuração do socket do cliente
host = 'localhost'
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

# Início da thread para receber dados contínuos
thread = threading.Thread(target=receive_data, args=(client_socket,))
thread.start()

# Execução do Streamlit
if __name__ == "__main__":
    streamlit_dashboard()

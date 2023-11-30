import socket
import time
import random

sensor_id = "SENSOR3"

sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sensor_socket.connect(('localhost', 5000))

while True:
    # Gerar dados aleatórios para sensor 3 (previsão do tempo)
    weather_forecast = random.choice(['Sunny', 'Cloudy', 'Rainy', 'Stormy'])
    data = f"WEATHER_FORECAST: {weather_forecast}: {sensor_id}"
    sensor_socket.send(data.encode())
    time.sleep(7)

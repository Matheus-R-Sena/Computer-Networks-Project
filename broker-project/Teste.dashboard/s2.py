import socket
import time
import random

sensor_id = "SENSOR2"

sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sensor_socket.connect(('localhost', 5000))

while True:
    # Gerar dados aleatórios para sensor 2 (umidade)
    humidity = random.uniform(0, 100)
    data = f"HUMIDITY: {humidity}: {sensor_id}"
    sensor_socket.send(data.encode())
    time.sleep(5)

import socket
import time
import random

sensor_id = "SENSOR1"

sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sensor_socket.connect(('localhost', 5000))

while True:
    # Gerar dados aleatórios para sensor 1 (temperatura)
    temperature = random.uniform(0, 100)
    data = f"TEMPERATURE: {temperature}: {sensor_id}"
    sensor_socket.send(data.encode())
    time.sleep(3)

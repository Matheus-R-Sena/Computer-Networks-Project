import re

numero = "2"
palavra = "amor"
padrao = r"\d+"


if re.search(padrao, numero):
    numero = int(numero)
    numero += 1
    print(numero)


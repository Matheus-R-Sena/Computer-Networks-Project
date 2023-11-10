import socket       # biblioteca para estabelecer as conexões
import argparse     # biblioteca para configurar os argumentos da linha de comando

#função para utilizar comandos de controle 
def comandos(comando):
    host = '0.0.0.0'   # endereço do servidor
    porta = 0        # porta do servidor

    try:
        # criação do socket TCP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # conexão com o servidor
        cliente.connect((host, porta))

        # verificação do comando 
        if comando == "LIST":

            # envia o comando para o servidor broker
            cliente.send("list".encode())

            # recebe uma mensagem de confirmação do servidor
            confirmacao = cliente.recv(1024).decode()

            # verifica a mensagem de confirmação
            if confirmacao == "confirmado":

                # recebe a lista de tópicos e assinantes e volta ela para o formato dicionário
                lista = cliente.recv(4096).decode()
                lista1 = eval(lista)

                # verifica se a lista esta vazia
                if not lista1:
                    print("lista vazia!")
                
                # imprime a lista de tópicos e seus respectivos assinantes
                else:
                    print("Comando aceito! Confira abaixo a lista de tópicos e seus assinantes:")
                    for topico, assinantes in lista1.items():
                        print(f'Tópico: {topico}')
                        for assinante in assinantes:
                            print(f'  Assinante: {assinante}')
                        print("")
                
            else:
                print("Comando não aceito pelo servidor")

        # caso o comando utilizado nao for o -c LIST ele imprimirá um erro
        else:
            print("Erro ao imprimir a lista, por favor utilize o comando: -c LIST")

    # exceções caso ocorra algo erro na conexão
    except Exception as e:
        print(f"Erro na conexão: {e}")

    # encerra a conexão com o servidor
    finally:
        cliente.close()


# configuração dos argumentos da linha de comando
argumentos = argparse.ArgumentParser(description = "modulo brokerCom")
argumentos.add_argument("-c", help = "comando", required = True)
entrada = argumentos.parse_args()
comandos(entrada.c)
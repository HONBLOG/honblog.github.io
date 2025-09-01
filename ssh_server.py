import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, ".test_rsa.key"))

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'Administrator') and (password == 'root'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

def main():
    server = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    ssh_port = int(sys.argv[2]) if len(sys.argv) > 2 else 2222

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print(f"[*] Listening for connection on {server}:{ssh_port} ...")

    client, addr = sock.accept()
    print(f"[*] Got a connection from {addr[0]}:{addr[1]}")

    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException:
        print('*** SSH negotiation failed.')
        sys.exit(1)

    chan = bhSession.accept(20)
    if chan is None:
        print('*** No channel.')
        sys.exit(1)
    print('[*] Authenticated!')
    print(chan.recv(1024).decode())
    chan.send(b'Welcome to bh_ssh')

    try:
        while True:
            command = input('Enter command: ')
            if command != 'exit':
                chan.send(command.encode())
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send(b'exit')
                print('exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()

if __name__ == '__main__':
    main()
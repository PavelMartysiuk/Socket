#send book yield
from os import path
#
from socket import socket

client = socket()
client.connect(('192.168.100.3', 5000))

while True:
    print('1) send a book \n2)found book')
    helpy = int(input('choose 1 or 2'))
    if helpy == 1:
        client.send(b'~')
        folder = input('enter folder')
        file = input ('enter book')
        client.send(file.encode())
        file =  file + '.txt'
        with open(path.join(f'./{folder}/' + file)) as file:
            book_cont = file.read()
        print(book_cont)
        for sym in book_cont:
            client.send(sym.encode())
        client.send(b'||')

    elif helpy == 2:

        number = input('enter the book')
        number = number.encode()
        client.send(number)
        content = b''
        while True:
            message = client.recv(1)
            if message == b'~':
                break
            content += message
        print(content.decode())


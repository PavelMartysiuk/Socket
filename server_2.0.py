from socket import socket
from select import select
from os import listdir
from os import path
from collections import defaultdict

server = socket()
server.bind(("192.168.100.3", 5000))
server.listen()
def gen_for_client_write(sock_client, book):
    for sym in book:
        sock_client.send(sym.encode())
        yield
    sock_client.send(b"~")
    
def gen_for_client_read(sock_client, books, to_listen):
    while True:
        content = b''
        helpy = 0
        message = sock_client.recv(3)
        if message == b'~':
            book_name = sock_client.recv(20)
            book_name = book_name.decode()
            helpy +=1
        if helpy == 1:
            #print(helpy)
            while True:
                try:
                data = sock_client.recv(1)
                #print(helpy)
                if data.decode('utf-8') == '||':
                    print('hi|')
                    with open(path.join(f'./books/{book_name}.txt','w')) as file:
                        file.write(content.decode('utf-8'))
                        break
                else:
                    content += data
                    #print('done')
                
        else:
            message = message.decode()
            message = int(message)
            book = books[message]
            with open('./books/' + book) as file:
                content = file.read()
            to_listen[sock_client].append(gen_for_client_write(sock_client, content))
            yield
            
def gen_to_accept_connect(to_listen, server):
    while True:
        client, addr = server.accept()
        print(f'accept connect to client - {addr}')
        to_listen[client] = [gen_for_client_read(client, books, to_listen)]
        yield

books = listdir('./books/')

to_listen = {}
to_listen[server] = [gen_to_accept_connect(to_listen, server)]

while True:
    ready_to_read, ready_to_write, _ =   select(to_listen, to_listen, [])
    
    for sock in ready_to_read:
        next(to_listen[sock][0])
        
    for sock in ready_to_write:
        if len(to_listen[sock]) > 1:
            try:
                next(to_listen[sock][1])
            except StopIteration:
                print('done sending for client')
                to_listen[sock].remove(to_listen[sock][1])

import threading
import socket
from person import Person

host = "127.0.0.1" 
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (host, port)
server.bind(ADDR)
server.listen(5)



persons = []
nicknames = []



def broadcast(message):
    for person in persons:
        person.send(message)

def handle(person):
    client = person.client
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = persons.index(client)
            persons.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast("{} left the chat!".format(nickname).encode("ascii"))
            print(f"{nickname} left the chat!".encode("utf-8"))
            nicknames.remove(nickname)
            break

def receive():
    while True:
       client, address = server.accept()
       person = Person(address, client)
       client = person.client
       name = person.name
       print("connected with {}".format(str(address)))

       client.send("NICK".encode("ascii"))
       nickname = client.recv(1024).decode("utf-8")
       nicknames.append(nickname)
       persons.append(client)

       print("nickname of the client is {}".format(nickname))
       broadcast("{} joined to server!!!".format(nickname).encode("ascii"))
       #client.send("connected to the server ".encode("ascii"))
       
       thread = threading.Thread(target=handle, args=(person,))
       thread.start()
print("server is listeniing..")
receive()
           





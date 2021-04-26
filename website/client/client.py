import socket
import threading


class Client:

    
    host = "127.0.0.1"
    port = 55555
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lock = threading.Lock()
    

    def __init__(self, nickname):
        self.client.connect((self.host, self.port))
        self.nickname = nickname

        self.messages = []

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write, args=(None,))
        write_thread.start()

    def disconnect(self):
        self.client.close()


    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode("utf-8")
                if message == "NICK":
                    self.client.send(self.nickname.encode("utf-8"))
                else:
                    self.lock.acquire()
                    self.messages.append(message)
                    self.lock.release()
                    print(message)
            except:
                print("an error occurred :(")
                self.client.close()
                break

    def get_messages(self):
            messages_copy = self.messages[:]

            # make sure memory is safe to access
            self.lock.acquire()
            self.messages = []
            self.lock.release()

            return messages_copy


    def write(self,msg):
        message = f"{self.nickname}: {msg}" 
        self.client.send(message.encode("utf-8"))



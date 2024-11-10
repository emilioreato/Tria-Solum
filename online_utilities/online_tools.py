import socket
import requests


class Online:

    public_ip = None

    def __init__(self):
        self.mode = "undefined"  # can be "server" or "client"
        pass

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))  # Using the Google DNS server
            local_ip = s.getsockname()[0]  # Get the local IP address
        finally:
            s.close()  # Cerrar el socket
        return local_ip

    @staticmethod
    def get_public_ip():
        try:
            response = requests.get('https://api.ipify.org?format=json')  # ask the webpage for an information
            if response.status_code == 200:  # satus code being "200" means that the connection was succesful, just convention.
                public_ip = response.json()['ip'].strip()  # converts the json response to a python dict and then searches for the "ip" value.
                return public_ip
            else:
                return "Couldnt get public IP from API. You can look up your IP on the internet and that also works"
        except Exception as e:
            return f"Error: {e}"


class Server(Online):  # a class that contains all the functions and utilities to be able to set a connection between two computers

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a socket obj
        self.mode = "server"
        self.manager = None

    def send(self, message, delimiter=";"):  # ; is a delimiter so that it can separete different messages
        self.manager.send((message+delimiter).encode('utf-8'))  # sending utf-8 encoded messages
        # print((message+delimiter))

    def send_not_encoded(self, info_to_send):  # ; is a delimiter so that it can separete different messages
        self.manager.send(info_to_send)  # sending utf-8 encoded messages

    def recieve(self):
        return self.manager.recv(1024).decode("utf-8")  # getting utf-8 encoded messages that were sent to us

    def recieve_not_encoded(self):
        return self.manager.recv(1024)

    def close(self):  # i think this can only be used by the server side
        self.manager.close()

    def set_up_server(self, PORT):  # port is tipically 8050

        self.socket.bind(("0.0.0.0", PORT))  # setting up the socket ///"localhost"

    def server_wait_for_connection(self):
        self.socket.listen(1)  # now we accept entring connections

        print("Waiting for the oppenent to join.")

        self.manager, _ = self.socket.accept()  # creating a client obj to recieve data


class Client(Online):

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a socket obj
        self.mode = "client"

    def send(self, message, delimiter=";"):  # ; is a delimiter so that it can separete different messages
        self.socket.send((message+delimiter).encode('utf-8'))  # sending utf-8 encoded messages
        # print((message+delimiter))

    def send_not_encoded(self, info_to_send):  # ; is a delimiter so that it can separete different messages
        self.socket.send(info_to_send)  # sending utf-8 encoded messages

    def recieve(self):
        return self.socket.recv(1024).decode("utf-8")  # getting utf-8 encoded messages that were sent to us

    def recieve_not_encoded(self):
        return self.socket.recv(1024)

    def set_up_client(self, HOST_IP, PORT):  # port is tipically 8050. ip has to be the public ip from the user creating the match(working as server)

        self.socket.connect((HOST_IP, PORT))

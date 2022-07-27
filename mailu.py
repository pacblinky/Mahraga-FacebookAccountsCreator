from paramiko import SSHClient, SSHException

class Mailu:
    def __init__(self,host,port,username,password):
        self.client = SSHClient()
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        try:
            self.client.connect(self.host,self.port,self.username,self.password)
            return True
        except Exception:
            return False

    def addUser(self,username,password):
        try:
            self.client.exec_command(f"docker-compose -f /mailu/docker-compose.yml exec admin flask mailu user {username} mahraga.com '{password}'")
            return True
        except Exception:
            return False

    def disconnect(self):
        self.client.close()


    
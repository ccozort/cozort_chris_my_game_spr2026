import socket

CLIENT_HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
CLIENT_PORT = 28765        # Port to listen on (non-privileged ports are > 1023)
MSGLEN = 1024
HOST = '10.11.57.246'  # Standard loopback interface address (localhost)
PORT = 28765        # Port to listen on (non-privileged ports are > 1023)
MSGLEN = 1024

class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)
    
if __name__ == "__main__":
    s = MySocket()
    s.connect(HOST, PORT)
    # s.mysend(b'Hello, world')
    # print(s.myreceive())
    # s.sock.close()
    # s.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect(CLIENT_HOST, CLIENT_PORT)
    # s.mysend(b'Hello, client')
    # print(s.myreceive())
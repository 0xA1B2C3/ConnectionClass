import socket

class TCP:
    def __init__(self, host, port):
        """Define a TCP Connection"""
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.s.setblocking(0)
        self.advpostheader = "POST %s HTTP/1.1\r\nHost: %s:%s\r\n"
        self.httpform = "application/x-www-form-urlencoded"
        return
    def send(self, msg):
        """Send a string of data"""
        return self.s.send(bytes(msg, "utf-8"))
    def get(self, path):
        return self.s.send(bytes("GET "+path+" HTTP/1.1\r\nHost: "+self.host+"\r\n\r\n", "utf-8"))
    def post(self, path, data):
        content = "application/x-www-form-urlencoded"
        req = bytes("POST "+path+" HTTP/1.1\r\nHost: "+self.host
                    +":"+str(self.port)+"\r\nContent-Length: "+str(len(data))+
                    "\r\n"+"Content-Type: "+content+"\r\n\r\n"+data, "utf-8")
        return self.s.send(req)
    def adv_post(self, path, args, varlist):
        data = self.advpostheader % (path, self.host, str(self.port))
        for head in args:
            data += "%s: %s\r\n" % (head, args[head])
        first = 1
        content = ""
        for var in varlist:
            if first == 0:
                content += "&"
            content += "%s=%s" % (var, varlist[var])
            first = 0
        data += "Content-Length: %s\r\n\r\n" % (str(len(content)))   
        data += content
        return self.s.send(data.encode())
    def recv(self):
        return self.s.recv(2048)
    def recvall(self):
        buf = b""
        add = b""
        while True:
            add = self.s.recv(2048)
            buf += add
            if add == b"":
                break
        return buf
    def close(self):
        self.s.close()
        return

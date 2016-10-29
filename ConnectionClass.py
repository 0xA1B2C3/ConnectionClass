import socket

#k9 = "license.k9webprotection.com"
#k9port = 80
#k9args = {"Connection": "close", "User-Agent": "K9 Web Protection 4.5.1001",
#          "Content-Type": "application/x-www-form-urlencoded"}
#k9vars = {"ul": "K997Y8D7EB",
#          "e": "1483208249dd6d102b57723fe49a0a3a792189e7541d5f9f1117817c00f299005d9b47117817c00f2990173a0020c7bc3f00f299014c666523c68d6011936503218661429cad0ad219a08f938502b2c091fdd7cd0bb26cd174843e011837b1e70e72220c50613a78f1023f5e613f332b06c5b060b218c11f855b81e0e25709e8ec61bceaf4"}

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

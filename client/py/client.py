import socket
import sys
sys.path.append("../../logic")

import base
import parseProtocol
from cryptManager import gCrypt

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8300))
    gCrypt.setAESKey("BanServer2018020")

    req = parseProtocol.ReqLogin()
    req.userid = "test01"
    req.password = "123456"
    buf = req.pack()
    data = gCrypt.encryptAES(buf)
    sock.send(data)

    recvBuf = sock.recv(1024)
    print recvBuf
    recvData = gCrypt.decryptAES(recvBuf)
    print base.getBytes(recvData)
    resp = parseProtocol.RespLogin()
    resp.make(recvData)
    print "flag=%d,numid=%d" % (resp.flag,resp.numid)
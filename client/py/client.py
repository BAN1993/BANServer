#encoding:utf-8

import socket
import sys
sys.path.append("../../logic")

import base
import parseProtocol
from cryptManager import gCrypt

if __name__ == '__main__':
#    gCrypt.setAESKey("BanServer2018020")
#    req = parseProtocol.ReqLogin()
#    req.userid = "test1"
#    req.password = "123456"
#    buf = req.pack()
#
#    packlen = base.getPackLen(buf)
#    data = buf[0:packlen+4]
#    ret, xyid, packlen, buf = base.getXYHand(data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8300))
    #sock.connect(('106.14.144.43', 8300))
    gCrypt.setAESKey("BanServer2018020")

    req = parseProtocol.ReqLogin()
    req.userid = "test1"
    req.password = "123456"
    buf = req.pack()
    buf = buf+buf
    sock.sendall(buf)

    recvBuf = sock.recv(1024)
    print recvBuf
    #recvData = gCrypt.decryptAES(recvBuf)
    ret, xyid, packlen, buf = base.getXYHand(recvBuf)
    print base.getBytes(buf)
    resp = parseProtocol.RespLogin()
    resp.make(buf[0:packlen])
    print "flag=%d,numid=%d" % (resp.flag,resp.numid)
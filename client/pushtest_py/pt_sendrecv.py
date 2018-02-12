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

    if len(sys.argv) != 3 :
        print("args error")
        exit()

    begin = int(sys.argv[1])
    end = int(sys.argv[2])
    print("begin=%d,end=%d" % (begin,end))

    req = parseProtocol.ReqRegister()
    req.password = "123456"

    for i in range(begin,end):
        req.userid = "test%d" % i
        buf = req.pack()
        begin = base.getMSTime()
        sock.send(buf)
        recvBuf = sock.recv(1024)
        ret, xyid, packlen, buf = base.getXYHand(recvBuf)
        resp = parseProtocol.RespRegister()
        resp.make(buf[0:packlen])
        end = base.getMSTime()
        print "flag=%d,numid=%d,slowtime=%d" % (resp.flag, resp.numid,end-begin)

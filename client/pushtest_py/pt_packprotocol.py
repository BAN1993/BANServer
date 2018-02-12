import socket
import ConfigParser
import sys
sys.path.append("../../logic")

import base
import parseProtocol
from cryptManager import gCrypt

if __name__ == '__main__':
    conf = ConfigParser.ConfigParser()
    conf.read('../../config.ini')
    gCrypt.init(conf)

    testCount = 10000
    if len(sys.argv) == 2:
        testCount = int(sys.argv[1])
    print "testCount=%d" % testCount

    begin = base.getMSTime()
    for i in range(0,testCount):
        req = parseProtocol.ReqRegister()
        req.userid = "test1"
        req.password = "123456"
        reqbuf = req.pack()
    end = base.getMSTime()
    print "pack use time=%d" % (end-begin)

    req = parseProtocol.ReqRegister()
    req.userid = "test1"
    req.password = "123456"
    reqbuf = req.pack()

    begin = base.getMSTime()
    for i in range(0, testCount):
        ret, xyid, packlen, buf = base.getXYHand(reqbuf)
        resp = parseProtocol.ReqRegister()
        resp.make(buf[0:packlen])
    end = base.getMSTime()
    print "make use time=%d" % (end - begin)
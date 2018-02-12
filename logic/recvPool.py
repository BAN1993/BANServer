import logging

import base
import selectProtocol

class recvPool(object):
    recvBuf = {}

    def delPlayer(self, conn):
        if conn in self.recvBuf:
            del self.recvBuf[conn]

    def push(self, conn, data):
        if conn not in self.recvBuf:
            self.recvBuf[conn] = ""
        self.recvBuf[conn] += data
        while True:
            if not self.parser(conn):
                break

    def parser(self, conn):
        if conn not in self.recvBuf:
            return False
        packlen = base.getPackLen(self.recvBuf[conn])
        if packlen <= 0:
            return False
        if packlen+base.LEN_INT > len(self.recvBuf[conn]):
            return False
        data = self.recvBuf[conn][0:packlen+base.LEN_INT]
        self.recvBuf[conn] = self.recvBuf[conn][packlen+base.LEN_INT:]
        ret, xyid, packlen, buf = base.getXYHand(data)
        if ret:
            selectProtocol.getXY(conn, xyid, buf[0:packlen])
        else:
            return False
        return True

gRecvPool  = recvPool()
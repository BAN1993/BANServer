import struct
import logging

LEN_INT = 4

class protocolException(RuntimeError):
	def __init__(self, arg):
		self.msg = arg

class protocolBase(object):
	bs_nowindex = 0
	bs_buf = ""

	def __init__(self):
		self.bs_nowindex = 0;
		self.bs_buf = ""

	#------------------------------------------------------------------------------------------------------------------------
	def makeBegin(self,buf):
		self.bs_nowindex = 0
		self.bs_buf = buf

	def getInt(self):
		if len(self.bs_buf) < self.bs_nowindex + LEN_INT:
			raise protocolException("data len err,datalen=" + str(len(self.bs_buf)) + ",aimlen=" + str(self.bs_nowindex + LEN_INT))
		(ret,) = struct.unpack('i', self.bs_buf[self.bs_nowindex : self.bs_nowindex + LEN_INT])
		self.bs_nowindex += LEN_INT
		return ret

	def getStr(self):
		strlen = self.getInt()
		if len(self.bs_buf) < self.bs_nowindex + strlen:
			raise protocolException("data len err,datalen=" + str(len(self.bs_buf)) + ",aimlen=" + str(self.bs_nowindex + strlen))
		(ret,) = struct.unpack(str(strlen) + "s", self.bs_buf[self.bs_nowindex : self.bs_nowindex + strlen])
		self.bs_nowindex += strlen
		return ret

	# ------------------------------------------------------------------------------------------------------------------------
	def packBegin(self,xyid):
		self.bs_nowindex = 0
		self.bs_buf = struct.pack("ii", xyid, 0)

	def packInt(self,num):
		self.bs_buf = self.bs_buf + struct.pack("i", num)

	def packStr(self,str):
		strlen = len(str)
		self.bs_buf = self.bs_buf + struct.pack("i"+str(strlen)+"s",strlen,str)

	def packEnd(self):
		return self.bs_buf


def getBytes(data):
	return ' '.join(['0x%x' % ord(x) for x in data])

def getBytesIndex(data,begin,strlen):
	if len(data)<begin+strlen:
		logging.error("data len<"+str(begin+strlen))
		return ""
	return ' '.join(['0x%x' % ord(data[x]) for x in range(begin,begin+strlen)])

def getHand(data):
	if len(data)<LEN_INT*2:
		return False,0,0
	(xyid,packlen,) = struct.unpack('ii',data[0:0+LEN_INT*2])
	if xyid <= 0 or packlen <=0:
		return False,xyid,packlen
	return True,xyid,packlen



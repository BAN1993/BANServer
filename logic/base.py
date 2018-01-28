import struct

LEN_INT = 4
LEN_FLOAT = 4

class protocolException(RuntimeError):
    def __init__(self, arg):
        self.msg = arg

def getBytes(data):
	return ' '.join(['0x%x' % ord(x) for x in data])

def getBytesIndex(data,begin,strlen):
	if len(data)<begin+strlen:
		log.loge("data len<"+str(begin+strlen))
		return ""
	return ' '.join(['0x%x' % ord(data[x]) for x in range(begin,begin+strlen)])

def getHand(data):
	if len(data)<LEN_INT*2:
		return False,0,0
	(xyid,packlen,) = struct.unpack('ii',data[0:0+LEN_INT*2])
	if xyid <= 0 or packlen <=0:
		return False,xyid,packlen
	return True,xyid,packlen
	
def getInt(data,index):
	if len(data)<index+LEN_INT:
		raise protocolException("getInt:data len err,datalen="+str(len(data))+",aimlen="+str(index+LEN_INT))
	(ret,) = struct.unpack('i',data[index:index+LEN_INT])
	return index+LEN_INT,ret

def getFloat(data,index):
	if len(data)<index+LEN_FLOAT:
		raise protocolException("getFloat:data len err,datalen=" + str(len(data)) + ",aimlen=" + str(index + LEN_FLOAT))
	(ret,) = struct.unpack('f', data[index:index + LEN_FLOAT])
	return index + LEN_FLOAT, ret

def getStr(data,index,strlen):
	if len(data)<index+strlen:
		raise protocolException("getStr:data len err,datalen="+str(len(data))+",aimlen="+str(index+strlen))
	(ret,) = struct.unpack(str(strlen)+"s",data[index:index+strlen])
	return index+strlen,ret

def getPackStr(cmd,*args):
	return struct.pack(cmd,*args)




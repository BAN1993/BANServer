import sys

import base
import log

HANLEN = 8

XYID_REQLOGIN	= 1
XYID_REQACTION	= 2
XYID_REQQUIT	= 3
XYID_REQDEFAULT	= 4
XYID_PLAYERDATA	= 5

class ReqLogin:
	numid = 0
	password = 0
	len_buf = 0
	buf = ""
	
	def make(self,xyid,packlen,data):
		try:
			nowindex,self.numid 	= base.getInt(data,0)
			nowindex,self.password 	= base.getInt(data,nowindex)
			nowindex,self.len_buf	= base.getInt(data,nowindex)
			nowindex,self.buf 		= base.getStr(data,nowindex,self.len_buf)
		except base.protocolException,e:
			log.loge(sys._getframe(),  "doLogin err,msg="+e.msg )
			return False
		return True
		
	def pack(self,numid,password,buf):
		data	= base.getPackStr("ii",XYID_REQLOGIN,0)
		data	= data + base.getPackStr("i",numid)
		data	= data + base.getPackStr("i",password)
		data	= data + base.getPackStr("i",len(buf))
		data	= data + base.getPackStr(str(len(buf))+"s",buf)
		return data

class ReqAction:
	actType = 0
	len_buf = 0
	buf = ""
	
	def make(self,xyid,packlen,data):
		try:
			nowindex,self.actType	= base.getInt(data,0)
			nowindex,self.len_buf	= base.getInt(data,nowindex)
			nowindex,self.buf		= base.getStr(data,nowindex,self.len_buf)
		except base.protocolException,e:
			log.loge(sys._getframe(),  "doAction err,msg="+e.msg)
			return False
		return True

class ReqQuit:
	num = 0
	
	def make(self,xyid,packlen,data):
		try:
			nowindex,self.num	= base.getInt(data,0)
		except base.protocolException,e:
			log.loge(sys._getframe(),  "doQuit err,msg="+e.msg)
			return False
		return True
	
	def pack(self,num):
		data	= base.getPackStr("ii",XYID_REQQUIT,0)
		data	= data + base.getPackStr("i",num)
		return data

class ReqDefault:
	num = 0
	
	def make(self,xyid,packlen,data):
		try:
			nowindex,self.num	= base.getInt(data,0)
		except base.protocolException,e:
			log.loge(sys._getframe(),  "doDefault err,msg="+e.msg)
			return False
		return True
		
class ReportPlayerData:
	numid = 0
	
	def pack(self,numid):
		data	= base.getPackStr("ii",XYID_PLAYERDATA,0)
		data	= data + base.getPackStr("i",numid)
		return data











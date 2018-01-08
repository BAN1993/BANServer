import logging

import base

HANLEN = 8

XYID_REQLOGIN	= 1
XYID_REQACTION	= 2
XYID_REQQUIT	= 3
XYID_REQDEFAULT	= 4
XYID_PLAYERDATA	= 5

class ReqLogin:
	numid = 0
	len_pas = 0
	password = ""
	
	def make(self,xyid,packlen,data):
		try:
			nowindex,self.numid 	= base.getInt(data,0)
			nowindex,self.len_pas 	= base.getInt(data,nowindex)
			nowindex,self.password	= base.getStr(data,nowindex,self.len_pas)
		except base.protocolException,e:
			logging.error("doLogin err,msg="+e.msg )
			return False
		return True
		
	def pack(self,numid,password):
		data	= base.getPackStr("ii",XYID_REQLOGIN,0)
		data	= data + base.getPackStr("i",numid)
		data	= data + base.getPackStr("i",len(password))
		data	= data + base.getPackStr(str(len(password))+"s",password)
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
			logging.error("doAction err,msg="+e.msg)
			return False
		return True

class ReqQuit:
	msg_len = 0
	msg = ""
	
	def make(self,xyid,packlen,data):
		try:
			nowindex,self.msg_len	= base.getInt(data,0)
			nowindex,self.msg		= base,getStr(data,nowindex,self.msg_len)
		except base.protocolException,e:
			logging.error("doQuit err,msg="+e.msg)
			return False
		return True
	
	def pack(self,msg):
		data	= base.getPackStr("ii",XYID_REQQUIT,0)
		data	= data + base.getPackStr("i",len(msg))
		data	= data + base.getPackStr(str(len(msg))+"s",msg)
		return data

class ReqDefault:
	num = 0
	
	def make(self,xyid,packlen,data):
		try:
			nowindex,self.num	= base.getInt(data,0)
		except base.protocolException,e:
			logging.error("doDefault err,msg="+e.msg)
			return False
		return True
		
class ReportPlayerData:
	numid = 0
	
	def pack(self,numid):
		data	= base.getPackStr("ii",XYID_PLAYERDATA,0)
		data	= data + base.getPackStr("i",numid)
		return data











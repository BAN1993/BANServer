import logging

import base

HANLEN = 8

XYID_REQLOGIN	= 1
XYID_REQACTION	= 2
XYID_REQQUIT	= 3
XYID_REQDEFAULT	= 4
XYID_PLAYERDATA	= 5

class ReqLogin(base.protocolBase):
	numid = 0
	password = ""
	
	def make(self,data):
		try:
			self.makeBegin(data[8:])
			self.numid = self.getInt()
			self.password = self.getStr()
		except base.protocolException,e:
			logging.error("doLogin err,msg="+e.msg )
			return False
		return True
		
	def pack(self,numid,password):
		self.packBegin(XYID_REQLOGIN)
		self.packInt(numid)
		self.packStr(password)
		return self.packEnd()

class ReqAction(base.protocolBase):
	actType = 0
	buf = ""
	
	def make(self,data):
		try:
			self.makeBegin(data[8:])
			self.actType = self.getInt()
			self.buf = self.getStr()
		except base.protocolException,e:
			logging.error("doAction err,msg="+e.msg)
			return False
		return True

class ReqQuit(base.protocolBase):
	msg = ""
	
	def make(self,data):
		try:
			self.makeBegin(data[8:])
			self.msg = self.getStr()
		except base.protocolException,e:
			logging.error("doQuit err,msg="+e.msg)
			return False
		return True
	
	def pack(self,msg):
		self.packBegin(XYID_REQQUIT)
		self.packStr(msg)
		return self.packEnd()

class ReqDefault(base.protocolBase):
	num = 0
	
	def make(self,data):
		try:
			self.makeBegin(data[8:])
			self.num = self.getInt()
		except base.protocolException,e:
			logging.error("doDefault err,msg="+e.msg)
			return False
		return True
		
class ReportPlayerData(base.protocolBase):
	numid = 0
	
	def pack(self,numid):
		self.packBegin(XYID_PLAYERDATA)
		self.packInt(numid)
		return self.packEnd()











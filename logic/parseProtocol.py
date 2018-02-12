import logging

import base

HANLEN = 8

XYID_REQLOGIN           = 1
XYID_RESPLOGIN          = 2
XYID_REQREGISTER        = 3
XYID_RESPREGISTER       = 4
XYID_REQQUIT        	= 4
XYID_PLAYERDATA	        = 6

class ReqLogin(base.protocolBase):
	numid = 0
	userid = ""
	password = ""
	
	def make(self, data):
		try:
			self.makeBegin(data[8:])
			self.numid = self.getInt()
			self.userid = self.getStr()
			self.password = self.getStr()
		except base.protocolException,e:
			logging.error("ReqLogin err,msg=" + e.msg)
			return False
		return True
		
	def pack(self):
		self.packBegin(XYID_REQLOGIN)
		self.packInt(self.numid)
		self.packStr(self.userid)
		self.packStr(self.password)
		return self.packEnd()

class RespLogin(base.protocolBase):
	FLAG = base.getEnum(SUCCESS=0,
	                    NOUSER=1,
	                    PWDERR=2,
	                    DBERR=3)
	flag = 0
	numid = 0

	def make(self, data):
		try:
			self.makeBegin(data[8:])
			self.flag = self.getInt()
			self.numid = self.getInt()
		except base.protocolException,e:
			logging.error("RespLogin err,msg=" + e.msg)
			return False
		return True

	def pack(self):
		self.packBegin(XYID_RESPLOGIN)
		self.packInt(self.flag)
		self.packInt(self.numid)
		return self.packEnd()

class ReqRegister(base.protocolBase):
	userid = ""
	password = ""

	def make(self, data):
		try:
			self.makeBegin(data[8:])
			self.userid = self.getStr()
			self.password = self.getStr()
		except base.protocolException,e:
			logging.error("ReqRegister err,msg=" + e.msg)
			return False
		return True

	def pack(self):
		self.packBegin(XYID_REQREGISTER)
		self.packStr(self.userid)
		self.packStr(self.password)
		return self.packEnd()

class RespRegister(base.protocolBase):
	FLAG = base.getEnum(SUCCESS=0,
	                    USED_USERID=1,
	                    DBERR=2,
	                    CREATEERR=3)
	flag = 0
	numid = 0

	def make(self, data):
		try:
			self.makeBegin(data[8:])
			self.flag = self.getInt()
			self.numid = self.getInt()
		except base.protocolException,e:
			logging.error("RespRegister err,msg=" + e.msg)
			return False
		return True

	def pack(self):
		self.packBegin(XYID_RESPREGISTER)
		self.packInt(self.flag)
		self.packInt(self.numid)
		return self.packEnd()


class ReqQuit(base.protocolBase):
	msg = ""
	
	def make(self, data):
		try:
			self.makeBegin(data[8:])
			self.msg = self.getStr()
		except base.protocolException,e:
			logging.error("doQuit err,msg=" + e.msg)
			return False
		return True
	
	def pack(self):
		self.packBegin(XYID_REQQUIT)
		self.packStr(self.msg)
		return self.packEnd()
		
class ReportPlayerData(base.protocolBase):
	numid = 0
	userid = ""
	
	def pack(self):
		self.packBegin(XYID_PLAYERDATA)
		self.packInt(self.numid)
		self.packStr(self.userid)
		return self.packEnd()











#import logging

import parseProtocol
from sendPool import gSendPool

class Player:
	
	#m_conn
	m_ip = ""
	m_port = 0
	m_numid = 0
	m_addr = ""
	
	def __init__(self, conn, numid):
		self.m_conn = conn
		self.m_ip = conn.getpeername()[0]
		self.m_port = conn.getpeername()[1]
		self.m_numid = numid
		self.m_addr = str(conn.getpeername())
		
#	def delPlayer(self):
#		self.conn.close()
		
	def getConn(self):
		return self.m_conn
		
	def getNumid(self):
		return self.m_numid
		
	def getAddr(self):
		return self.m_addr
		
	def senddata(self, data):
		gSendPool.push(self.m_conn, data)
		
	def close(self,data):
		req = parseProtocol.ReqQuit()
		senddata = req.pack()
		self.senddata(senddata)
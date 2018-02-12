#encoding:utf-8

import socket
import select
import Queue
import logging
import threading

#import base
#import selectProtocol
from serverLogic import gServerLogic
from sendPool import gSendPool
from recvPool import gRecvPool
from playerManager import gPlayerManager
from dbManager import gDBManager
from cryptManager import gCrypt

class Server(object):

	m_host = ''
	m_port = 0
	m_timeout = 2
	m_listenNum = 5
	m_maxBufLen = 1024
	
	m_server = None
	m_timer = None

	m_inputs = []
	m_outputs = []
	m_clientList = {}

	def __init__(self, conf):
		self.m_host			= str(conf.get("serverConfig", "host"))
		self.m_port			= int(conf.get("serverConfig", "port"))
		self.m_timeout		= int(conf.get("serverConfig", "timeout"))
		self.m_listenNum	= int(conf.get("serverConfig", "listennum"))
		self.m_maxBufLen	= int(conf.get("serverConfig", "maxbuflen"))
		logging.info("host=%s,port=%d,timeout=%d,listennum=%d,maxbuflen=%d" % (self.m_host, self.m_port, self.m_timeout, self.m_listenNum, self.m_maxBufLen))

		self.m_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.m_server.setblocking(False)
		self.m_server.settimeout(self.m_timeout)
		self.m_server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #keepalive
		self.m_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #端口复用

		server_host = (self.m_host, self.m_port)
		self.m_server.bind(server_host)
		self.m_server.listen(self.m_listenNum)
		logging.info("bind success:host=" + str(server_host))
		self.m_inputs = [self.m_server]

		gCrypt.init(conf)
		gDBManager.init(conf)

	## def __init__(self, host, port, timeout=2, listennum=5):

	def onTimer(self):
		gServerLogic.onTimer()
		gDBManager.onTimer()

		self.m_timer = threading.Timer(1.0, self.onTimer)
		self.m_timer.start()

	def run(self):
		self.onTimer()

		while True:
			readtable, writable, exceptional = select.select(self.m_inputs, gSendPool.getOutPuts(), self.m_inputs, self.m_timeout)
			if not (readtable or writable or exceptional) :
				continue
			
			for s in readtable:
				if s is self.m_server:
					conn, addr = s.accept()
					logging.info("accept=%s,addr=%s" % (str(conn), str(addr)))
					conn.setblocking(0)
					self.m_inputs.append(conn)
					self.m_clientList[conn] = str(addr)
				else:
					data = ""
					try:
						data = s.recv(self.m_maxBufLen)
						logging.debug("recv data=" + data)
					except socket.error, msg:
						logging.error("SocketError Code=" + str(msg))
					if data:
						gRecvPool.push(s,data)
					else:
						logging.info("client close=%s,addr=%s" % (str(s), str(self.m_clientList[s])))
						if s in self.m_inputs:
							self.m_inputs.remove(s)
						s.close()
						del self.m_clientList[s]
						gPlayerManager.delPlayerByConn(s)
				## if s is self.m_server:
			## for s in readtable:
			
			for s in writable:
				try:
					next_msg = gSendPool.getMsg(s)
				except Queue.Empty:
					logging.debug("Output Queue is Empty!conn=" + self.m_clientList[s])
				except Exception, e:
					logging.error("Send Data Error! ErrMsg:%s" % str(e))
				else:
					try:
						s.sendall(next_msg)
						#logging.debug("send data:addr=%s,data=%s" % (str(s.getpeername()),next_msg))
					except Exception, e:
						logging.error("Send Data to %s  Error And Close! ErrMsg:%s" % (str(s.getpeername()), str(e)))
						gPlayerManager.delPlayerByConn(s)
			## for s in writable:
			
			for s in exceptional:
				logging.error("Client:%s Close Error." % str(self.m_clientList[s]))
				if s in self.m_inputs:
					self.m_inputs.remove(s)
					s.close()
				del self.m_clientList[s]
			## for s in exceptional:
	## def run(self):



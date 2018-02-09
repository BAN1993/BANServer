#encoding:utf-8

import socket
import select
import Queue
import logging
import threading

import base
import selectProtocol
from serverLogic import gServerLogic
from sendPool import gSendPool
from playerManager import gPlayerManager
from dbManager import gDBManager

class Server(object):

	m_host = ''
	m_port = 0
	m_timeout = 2
	m_listenNum = 5
	m_maxBufLen = 1024
	
	m_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
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
		try:
			server_host = (self.m_host, self.m_port)
			self.m_server.bind(server_host)
			self.m_server.listen(self.m_listenNum)
			logging.info("bind success:host="+str(server_host))
		except :
			raise
		self.m_inputs = [self.m_server]

		try:
			gDBManager.mConnect(conf)
		except:
			raise

	## def __init__(self, host, port, timeout=2, listennum=5):

	def onTimer(self):
		gServerLogic.onTimer()
		gDBManager.onTimer()

		bo, row, ret = gDBManager.select("select * from players")
		logging.debug("row=%d" % row)
		if bo :
			for k in ret:
				logging.debug(str(k[0])+":"+str(k[1])+":"+str(k[2]))

		self.timer = threading.Timer(1.0, self.onTimer)
		self.timer.start()

	def run(self):
		self.onTimer()
		while True:
			readtable, writable, exceptional = select.select(self.m_inputs, gSendPool.getOutPuts(), self.m_inputs, self.m_timeout)
			if not (readtable or writable or exceptional) :
				continue
			
			for s in readtable:
				if s is self.m_server:
					conn, addr = s.accept()
					logging.info("accept:"+str(conn)+",addr="+str(addr))
					conn.setblocking(0)
					self.m_inputs.append(conn)
					self.m_clientList[conn]=str(addr)
				else:
					data = ""
					try:
						data = s.recv(self.m_maxBufLen)
						#logging.debug("recv data="+base.getBytes(data))
					except socket.error, msg:
						logging.error('Recv Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
					if data:
						ret,xyid,packlen = base.getHand(data)
						if ret == True:
							#logging.debug("len="+str(packlen)+",by="+base.getBytes(data[0:packlen]))
							selectProtocol.getXY(s,xyid,data[0:packlen])
						#else:
							#logging.error("can not getHand,data="+base.getBytes(data))
					else:
						logging.info("client colse:"+str(s)+",addr="+str(self.m_clientList[s]))
						if s in self.m_inputs:
							self.m_inputs.remove(s)
						s.close()
						del self.m_clientList[s]
						gPlayerManager.delPlayerByConn(s)
				## if s is self.m_server:
			## for s in readtable:
			
			for s in writable:
				#logging.debug("get send msg:conn="+self.m_clientList[s]+",nowsize="+str(self.m_msgQueus[s].qsize()))
				try:
					next_msg = gSendPool.getMsg(s)
				except Queue.Empty:
					logging.debug("Output Queue is Empty!conn="+self.m_clientList[s])
					#self.m_outputs.remove(s)
				except Exception, e:
					logging.error("Send Data Error! ErrMsg:%s" % str(e))
				else:
					try:
						s.sendall(next_msg)
						#logging.debug("send data:addr=%s,databytes=%s" % (str(s.getpeername()),base.getBytes(next_msg)))
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



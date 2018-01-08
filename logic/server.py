#encoding:utf-8

import socket
import select
import Queue
import logging

import base
import selectProtocol
import sendPool
import playerManager

class Server(object):

	m_host = ''
	m_port = 0
	m_timeout = 2
	m_lisenNum = 5
	m_maxBufLen = 1024
	
	m_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	m_inputs = []
	m_outputs = []
	m_clientList = {}
	
	def __init__(self, host, port, timeout=2, listennum=5):
		self.m_host			= host
		self.m_port			= port
		self.m_timeout		= timeout
		self.m_lisenNum		= listennum
		self.m_maxBufLen	= 1024
		
		self.m_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.m_server.setblocking(False)
		self.m_server.settimeout(self.m_timeout)
		self.m_server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #keepalive
		self.m_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #¶Ë¿Ú¸´ÓÃ
		try:
			server_host = (self.m_host, self.m_port)
			self.m_server.bind(server_host)
			self.m_server.listen(self.m_lisenNum)
			logging.info("bind success:host="+str(server_host))
		except :
			raise
		self.m_inputs = [self.m_server]
	## def __init__(self, host, port, timeout=2, listennum=5):

	def run(self):
		while True:
			readtable, writable, exceptional = select.select(self.m_inputs, sendPool.getOutPuts(), self.m_inputs, self.m_timeout)
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
							logging.debug("len="+str(packlen)+",by="+base.getBytes(data[0:packlen]))
							selectProtocol.getXY(s,xyid,packlen,data[0:packlen])
						#else:
							#logging.error("can not getHand,data="+base.getBytes(data))
					else:
						logging.info("client colse:"+str(s)+",addr="+str(self.m_clientList[s]))
						if s in self.m_inputs:
							self.m_inputs.remove(s)
						s.close()
						del self.m_clientList[s]
						playerManager.delPlayerByConn(s)
				## if s is self.m_server:
			## for s in readtable:
			
			for s in writable:
				#logging.debug("get send msg:conn="+self.m_clientList[s]+",nowsize="+str(self.m_msgQueus[s].qsize()))
				try:
					next_msg = sendPool.getMsg(s)
				except Queue.Empty:
					logging.debug("Output Queue is Empty!conn="+self.m_clientList[s])
					#self.m_outputs.remove(s)
				except Exception, e:
					logging.error("Send Data Error! ErrMsg:%s" % str(e))
				else:
					try:
						s.sendall(next_msg)
						logging.debug("send data:addr=%s,databytes=%s" % (str(s.getpeername()),base.getBytes(next_msg)))
					except Exception, e:
						logging.error("Send Data to %s  Error And Close! ErrMsg:%s" % (str(s.getpeername()), str(e)))
						playerManager.delPlayerByConn(s)
			## for s in writable:
			
			for s in exceptional:
				logging.error("Client:%s Close Error." % str(self.m_clientList[cli]))
				if s in self.m_inputs:
					self.m_inputs.remove(s)
					s.close()
				del self.m_clientList[s]
			## for s in exceptional:
	## def run(self):



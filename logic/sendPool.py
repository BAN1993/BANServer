import Queue
import logging

import player
#from playerManager import gPlayerManager

class sendPool(object):
	msgQueus = {}
	msgOutPuts = []

	def delPlayer(self, conn):
		logging.debug("conn="+str(conn))
		if conn in self.msgQueus:
			del self.msgQueus[conn]
		if conn in self.msgOutPuts:
			del self.msgOutPuts[conn]

	def push(self, conn, data):
		if conn not in self.msgQueus:
			self.msgQueus[conn] = Queue.Queue()
		if conn not in self.msgOutPuts:
			self.msgOutPuts.append(conn)
		self.msgQueus[conn].put(data)

	def getOutPuts(self):
		return self.msgOutPuts

	def getMsg(self, conn):
		#logging.debug("addr="+str(conn.getpeername()))
		try:
			return self.msgQueus[conn].get_nowait()
		except:
			if conn in self.msgOutPuts:
				self.msgOutPuts.remove(conn)
			raise

gSendPool = sendPool()
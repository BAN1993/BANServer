import Queue
import logging

import player
#from playerManager import gPlayerManager

class sendPool(object):
	msgQueus = {}
	msgOutPuts = []

	def delPlayer(self, conn):
		if conn in self.msgQueus:
			del self.msgQueus[conn]
		if conn in self.msgOutPuts:
			index = self.msgOutPuts.index(conn)
			del self.msgOutPuts[index]

	def push(self, conn, data):
		if conn not in self.msgQueus:
			self.msgQueus[conn] = Queue.Queue()
		if conn not in self.msgOutPuts:
			self.msgOutPuts.append(conn)
		self.msgQueus[conn].put(data)

	def getOutPuts(self):
		return self.msgOutPuts

	def getMsg(self, conn):
		logging.debug("addr="+str(conn.getpeername()))
		try:
			#return self.msgQueus[conn].get_nowait()
			return self.msgQueus[conn].get()
		except:
			if conn in self.msgOutPuts:
				self.msgOutPuts.remove(conn)
			raise

gSendPool = sendPool()
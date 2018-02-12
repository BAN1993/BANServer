import logging

import player
import parseProtocol
from sendPool import gSendPool

class playerManager(object):
	playerList = {}  # k=numid,v=player

	def addPlayer(self, conn, numid):
		logging.info("numid=%d,try to add,conn=%s" % (numid, str(conn.getpeername())))
		if self.playerList.has_key(numid):
			logging.warning("numid=%d,is in list,colse it,conn=%s" % (numid, str(self.playerList[numid])))
			self.playerList[numid].close("kick by others")
			#self.playerList[numid].getConn().shutdown(2)
			#self.playerList[numid].getConn().close()
			del self.playerList[numid]
		pl = player.Player(conn, numid)
		self.playerList[numid] = pl
		logging.info("numid=%d,add to list,conn=%s" % (numid, str(conn.getpeername())))
		return True

	def delPlayer(self, tmpplayer):
		gSendPool.delPlayer(tmpplayer.getConn())
		numid = tmpplayer.getNumid()
		if self.playerList.has_key(numid):
			del self.playerList[numid]

	def findPlayerByConn(self, conn):
		for key in self.playerList:
			if self.playerList[key].getConn() == conn:
				return self.playerList[key]
		return False

	def delPlayerByConn(self, conn):
		tmpPlayer = self.findPlayerByConn(conn)
		if not tmpPlayer:
			logging.warning("Can not find player:conn=" + str(conn))
			return
		self.delPlayer(tmpPlayer)

	def findPlayer(self, numid):
		if self.playerList.has_key(numid):
			return self.playerList[numid]
		else:
			return False

	def broadcast(self, data):
		for key in self.playerList:
			self.playerList[key].senddata(data)

	def broadcastPlayerData(self, conn, numid):
		report = parseProtocol.ReportPlayerData()

		for key in self.playerList:
			if self.playerList[key].getConn() == conn:
				for key2 in self.playerList:
					if key2 != key:
						report.numid = self.playerList[key2].getNumid()
						# TODO add userid
						data = report.pack()
						logging.debug("numid=%d send numid=%d" % (self.playerList[key].getNumid(), self.playerList[key2].getNumid()))
						self.playerList[key].senddata(data)
			else:
				report.nuimd = numid
				data = report.pack()
				self.playerList[key].senddata(data)
				logging.debug("numid=%d send numid=%d" % (self.playerList[key].getNumid(), numid))

	def getPlayerCount(self):
		return len(self.playerList)

gPlayerManager = playerManager()




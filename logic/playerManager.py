import logging

import player
import parseProtocol
from sendPool import gSendPool

class playerManager(object):
	playerList = {}  # k=numid,v=player

	def addPlayer(self,conn,numid):
		logging.info("numid="+str(numid)+",try to add,conn="+str(conn.getpeername()))
		if self.playerList.has_key(numid) :
			logging.warning("numid="+str(numid)+",is in list,close it,conn="+str(self.playerList[numid]))
			self.playerList[numid].close("kick by others")
			#self.playerList[numid].getConn().shutdown(2)
			#self.playerList[numid].getConn().close()
			del self.playerList[numid]
		pl = player.Player(conn,numid)
		self.playerList[numid] = pl
		logging.info("numid="+str(numid)+",add to list,conn="+str(conn.getpeername()))
		return True

	def delPlayer(self,player):
		gSendPool.delPlayer(player.getConn())
		numid = player.getNumid()
		if self.playerList.has_key(numid):
			del self.playerList[numid]

	def findPlayerByConn(self,conn):
		for key in self.playerList:
			if self.playerList[key].getConn() == conn:
				return self.playerList[key]
		return False

	def delPlayerByConn(self,conn):
		tmpPlayer = self.findPlayerByConn(conn)
		if not tmpPlayer:
			#raise Exception("Can not find player:conn="+str(conn))
			logging.warning("Can not find player:conn="+str(conn))
			return
		self.delPlayer(tmpPlayer)

	def findPlayer(self,numid):
		if self.playerList.has_key(numid):
			return self.playerList[numid]
		else:
			return False

	def broadcast(self,data):
		for player in self.playerList.values:
			player.senddata(data)

	def broadcastPlayerData(self,conn,numid):
		logging.debug("numid="+str(numid))
		report = parseProtocol.ReportPlayerData()

		for key in self.playerList:
			if self.playerList[key].getConn() == conn:
				for key2 in self.playerList:
					if key2 != key:
						data = report.pack(self.playerList[key2].getNumid())
						logging.debug("numid="+str(self.playerList[key].getNumid())+" send numid="+str(self.playerList[key2].getNumid()))
						self.playerList[key].senddata(data)
			else:
				data = report.pack(numid)
				self.playerList[key].senddata(data)
				logging.debug("numid="+str(self.playerList[key].getNumid())+" send numid="+str(numid))

	def getPlayerCount(self):
		return len(self.playerList)

gPlayerManager = playerManager()




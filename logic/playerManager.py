import logging

import sendPool
import player
import parseProtocol

playerList = {}			#k=numid,v=player

def addPlayer(conn,numid):
	logging.info("addPlayer:numid="+str(numid)+",try to add,conn="+str(conn.getpeername()))
	if playerList.has_key(numid) :
		logging.warning("addPlayer:numid="+str(numid)+",is in list,close it,conn="+str(playerList[numid]))
		playerList[numid].close("kick by others")
		#playerList[numid].getConn().shutdown(2)
		#playerList[numid].getConn().close()
		del playerList[numid]
	pl = player.Player(conn,numid)
	playerList[numid] = pl
	logging.info("addPlayer:numid="+str(numid)+",add to list,conn="+str(conn.getpeername()))
	return True

def delPlayer(player):
	sendPool.delPlayer(player.getConn())
	numid = player.getNumid()
	if playerList.has_key(numid):
		del playerList[numid]

def findPlayerByConn(conn):
	for key in playerList:
		if playerList[key].getConn() == conn:
			return playerList[key]
	return False
		
def delPlayerByConn(conn):
	player = findPlayerByConn(conn)
	if player == False:
		#raise Exception("Can not find player:conn="+str(conn))
		logging.warning("delPlayerByConn:Can not find player:conn="+str(conn))
		return
	delPlayer(player)
		
def findPlayer(numid):
	if playerList.has_key(numid):
		return playerList[numid]
	else:
		return False
		
def broadcast(data):
	for player in playerList.values:
		player.senddata(data)
		
def broadcastPlayerData(conn,numid):
	logging.debug("broadcastPlayerData:numid="+str(numid))
	report = parseProtocol.ReportPlayerData()

	for key in playerList:
		if playerList[key].getConn() == conn:
			for key2 in playerList:
				if key2 != key:
					data = report.pack(playerList[key2].getNumid())
					logging.debug("broadcastPlayerData:numid="+str(playerList[key].getNumid())+" send numid="+str(playerList[key2].getNumid()))
					playerList[key].senddata(data)
		else:
			data = report.pack(numid)
			playerList[key].senddata(data)
			logging.debug("broadcastPlayerData:numid="+str(playerList[key].getNumid())+" send numid="+str(numid))






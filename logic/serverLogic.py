import logging

import player
import playerManager
import parseProtocol

def doLogin(conn,req):
	logging.info("numid="+str(req.numid)+",password="+req.password)
	if True == playerManager.addPlayer(conn,req.numid):
		playerManager.broadcastPlayerData(conn,req.numid)
		player.senddata("hellow")

def doAction(req):
	logging.info("acttype=%d,buf=%s" % (req.actType,req.buf))

def doQuit(req):
	logging.info("1")

def doDefault(req):
	logging.info("1")

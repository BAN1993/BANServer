import logging

import player
import playerManager
import parseProtocol

def doLogin(conn,req):
	logging.info("numid="+str(req.numid)+",password="+req.password)
	if True == playerManager.addPlayer(conn,req.numid):
		playerManager.broadcastPlayerData(conn,req.numid)
		player = playerManager.findPlayer(req.numid)

def doAction(req):
	logging.info("buf=%s" % (req.buf))

def doQuit(req):
	logging.info("1")

def doDefault(req):
	logging.info("1")

def doPosition(req):
	logstr = "x=%f,y=%f,z=%f" % (req.x,req.y,req.z)
	logging.info(logstr)
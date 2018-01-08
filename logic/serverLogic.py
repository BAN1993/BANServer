import logging

import player
import playerManager
import parseProtocol

def doLogin(conn,req):
	logging.info("doLogin:numid="+str(req.numid)+",password="+req.password)
	if True == playerManager.addPlayer(conn,req.numid):
		playerManager.broadcastPlayerData(conn,req.numid)

def doAction(req):
	logging.info("doAction:acttype=%d,buf=%s" % (req.actType,req.buf))

def doQuit(req):
	logging.info("doQuit")

def doDefault(req):
	logging.info("doDefault")

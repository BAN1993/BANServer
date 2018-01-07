import sys

import player
import playerManager
import log
import parseProtocol

def doLogin(conn,req):
	log.logi(sys._getframe(),"doLogin:numid="+str(req.numid)+",password="+req.password)
	if True == playerManager.addPlayer(conn,req.numid):
		playerManager.broadcastPlayerData(conn,req.numid)

def doAction(req):
	log.logi(sys._getframe(),"doAction:acttype=%d,buf=%s" % (req.actType,req.buf))

def doQuit(req):
	log.logi(sys._getframe(),"doQuit")

def doDefault(req):
	log.logi(sys._getframe(),"doDefault")

import logging

import player
import parseProtocol
from playerManager import gPlayerManager

class serverLogic(object):

	def onTimer(self):
		logging.info("player count="+str(gPlayerManager.getPlayerCount()))

	def doLogin(self, conn, req):
		logging.info("numid="+str(req.numid)+",password="+req.password)
		if gPlayerManager.addPlayer(conn,req.numid):
			gPlayerManager.broadcastPlayerData(conn,req.numid)
			#player = gPlayerManager.findPlayer(req.numid)

	def doAction(self, req):
		logging.info("acttype=%d,buf=%s" % (req.actType,req.buf))

	def doQuit(self, req):
		logging.info("1")

	def doDefault(self, req):
		logging.info("1")

gServerLogic = serverLogic()
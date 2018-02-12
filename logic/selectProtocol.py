import logging

import parseProtocol
from serverLogic import gServerLogic
import base

def getXY(conn, xyid, data):
	begin = base.getMSTime()
	if xyid == parseProtocol.XYID_REQLOGIN:
		req = parseProtocol.ReqLogin()
		ret = req.make(data)
		if ret:
			gServerLogic.doLogin(conn,req)

	elif xyid == parseProtocol.XYID_REQREGISTER:
		req = parseProtocol.ReqRegister()
		ret = req.make(data)
		if ret:
			gServerLogic.doRegister(conn,req)
			
	elif xyid == parseProtocol.XYID_REQQUIT:
		req = parseProtocol.ReqQuit()
		ret = req.make(data)
		if ret:
			gServerLogic.doQuit(req)
	## if xyid == **
	end = base.getMSTime()
	use = end - begin
	logging.info("slowtime=%d,xyid=%d" % (use, xyid))


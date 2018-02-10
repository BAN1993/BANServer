import parseProtocol
from serverLogic import gServerLogic

def getXY(conn,xyid,data):

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

	


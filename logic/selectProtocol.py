import base
import parseProtocol
import serverLogic

def getXY(conn,xyid,data):

	if xyid == parseProtocol.XYID_REQLOGIN:
		req = parseProtocol.ReqLogin()
		ret = req.make(data)
		if ret:
			serverLogic.doLogin(conn,req)
			
	elif xyid == parseProtocol.XYID_REQACTION:
		req = parseProtocol.ReqAction()
		ret = req.make(data)
		if ret:
			serverLogic.doAction(req)
			
	elif xyid == parseProtocol.XYID_REQQUIT:
		req = parseProtocol.ReqQuit()
		ret = req.make(data)
		if ret:
			serverLogic.doQuit(req)
			
	else:
		req = parseProtocol.ReqDefault()
		ret = req.make(data)
		if ret:
			serverLogic.doDefault(req)
	


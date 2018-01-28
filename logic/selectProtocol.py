import base
import parseProtocol
import serverLogic

def getXY(conn,xyid,packlen,data):

	if xyid == parseProtocol.XYID_REQLOGIN:
		req = parseProtocol.ReqLogin()
		ret = req.make(xyid,packlen,data[8:])
		if ret == True:
			serverLogic.doLogin(conn,req)
			
	elif xyid == parseProtocol.XYID_REQACTION:
		req = parseProtocol.ReqAction()
		ret = req.make(xyid,packlen,data[8:])
		if ret == True:
			serverLogic.doAction(req)
			
	elif xyid == parseProtocol.XYID_REQQUIT:
		req = parseProtocol.ReqQuit()
		ret = req.make(xyid,packlen,data[8:])
		if ret == True:
			serverLogic.doQuit(req)
			
	else:
		req = parseProtocol.ReqDefault()
		ret = req.make(xyid,packlen,data[8:])
		if ret == True:
			serverLogic.doDefault(req)
	


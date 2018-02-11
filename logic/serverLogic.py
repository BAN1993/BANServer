#encoding:utf-8

import logging

import parseProtocol
from playerManager import gPlayerManager
from dbManager import gDBManager
from sendPool import gSendPool

class serverLogic(object):

	def onTimer(self):
		a=1
		#logging.info("player count="+str(gPlayerManager.getPlayerCount()))
	## def onTimer(self):

	def doLogin(self, conn, req):
		logging.info("numid=%d,userid=%s,pwd=%s" % (req.numid,req.userid,req.password))

		resp = parseProtocol.RespLogin()
		resp.flag = resp.FLAG.SUCCESS

		sql = "select numid,passwd from players where userid='%s'" % req.userid
		ret, row, rslt = gDBManager.select(sql)
		if not ret:
			resp.flag = resp.FLAG.DBERR
			logging.error("select ret err,sql=%s" % sql)
		elif row <= 0:
			resp.flag = resp.FLAG.NOUSER
			logging.info("numid=%d,userid=%s select no data" % (req.numid, req.userid))
		else:
			if str(rslt[0][1]) == req.password :
				resp.numid = int(rslt[0][0])
				if gPlayerManager.addPlayer(conn, req.numid):
					gPlayerManager.broadcastPlayerData(conn, req.numid)
			else:
				resp.flag = resp.FLAG.PWDERR
				logging.info("numid=%d,userid=%s pwd err" % (req.numid, req.userid))

		logging.info("numid=%d,userid=%s,flag=%d" % (resp.numid,req.userid,resp.flag))
		data = resp.pack()
		gSendPool.push(conn, data)
	## def doLogin(self, conn, req):

	def doRegister(self, conn, req):
		logging.info("userid=%s,pwd=%s" % (req.userid,req.password))

		resp = parseProtocol.RespRegister()
		resp.flag = resp.FLAG.SUCCESS

		# 查询是否存在这个账号id
		sql = "select numid from players where userid='%s'" % req.userid
		ret, row, rslt = gDBManager.select(sql)
		if not ret:
			resp.flag = resp.FLAG.DBERR
			logging.error("select ret err,sql=%s" % sql)
		elif row>0:
			resp.flag = resp.FLAG.USED_USERID
			logging.info("userid=%s had been used" % req.userid)
		else:

			#插入这条账号数据
			sql = "insert into players(numid,userid,passwd) select ifnull(max(numid),0)+1,'%s','%s' from players" % (req.userid, req.password)
			ret, row, rslt = gDBManager.querry(sql)
			if not ret:
				resp.flag = resp.FLAG.DBERR
				logging.error("insert ret err,sql=%s" % sql)
			elif row>0:

				#查询这个账号id的数字id
				sql = "select numid from players where userid='%s'" % req.userid
				ret, row, rslt = gDBManager.select(sql)
				if not req:
					resp.flag = resp.FLAG.DBERR
					logging.error("select ret err,sql=%s" % sql)
				elif row<=0:
					resp.flag = resp.FLAG.CREATEERR
					logging.warning("insert success,bug select row<=0,userid=%s" % req.userid)
				else:
					resp.numid = int(rslt[0][0])
			else:
				resp.flag = resp.FLAG.CREATEERR
				logging.warning("insert row <=0,sql=%s" % sql)

		logging.info("userid=%s,numid=%d,flag=%d" % (req.userid,resp.numid,resp.flag))
		data = resp.pack()
		gSendPool.push(conn, data)

	def doQuit(self, req):
		logging.info("req=%s" % str(req))


gServerLogic = serverLogic()
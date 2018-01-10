#encoding:utf-8

import sys
import socket
import traceback
#from thread import *
import logging

sys
sys.path.append("logic")
import deamon
import server
import log

HOST = ''
PORT = 8300

if __name__ == '__main__':

	deamon.daemonize()
	log.initLog("logging.conf")
	logging.info("server start!!!")
	
	try:
		svr = server.Server(HOST,PORT)
	except socket.error, msg:
		logging.error('Bind failed,Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	
	try:
		svr.run()
	except BaseException as e:
		logging.exception(e)
	else:
		logging.error("Crash Unknown!")
    


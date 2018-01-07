#encoding:utf-8

import sys
import socket
import traceback
#from thread import *

sys
sys.path.append("logic")
import server
import log

HOST = ''
PORT = 8300

if __name__ == '__main__':

	log.logi(sys._getframe(),"server start!")
	
	try:
		svr = server.Server(HOST,PORT)
	except socket.error, msg:
		log.loge(sys._getframe(), 'Bind failed,Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	
	try:
		svr.run()
	except BaseException as e:
		log.logexc(e)
	else:
		log.loge("Crash Unknown!")
    


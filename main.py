#encoding:utf-8

import sys
import logging
import ConfigParser

sys
sys.path.append("logic")
import deamon
import server
import log

HOST = ''
PORT = 8300

if __name__ == '__main__':

	log.initLog("logging.conf")
	logging.info("server start!!!")

	deamon.daemonize()

	try:
		conf = ConfigParser.ConfigParser()
		conf.read('config.ini')
		svr = server.Server(conf)
		svr.run()
	except BaseException as e:
		logging.exception(e)
		exit()
	else:
		logging.error("Crash Unknown!")
		exit()


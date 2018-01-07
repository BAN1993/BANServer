import os
import sys
import logging
import time

global g_loglevel
g_loglevel = 0

LOG_LEVEL_DEBUG = 0
LOG_LEVEL_INFO = 1
LOG_LEVEL_WARNING = 2
LOG_LEVEL_ERROR = 3

def initLog(fname):
	if os.path.exists('log'):
		print "MyLog.init:log is exists"
	else:
		os.mkdir("log")
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s[%(levelname)s]%(message)s',
		datefmt='[%Y-%m-%d %H:%M:%S]',
		filename=('log/%s_%s.log' % (fname,time.strftime("%Y%m%d-%H%M%S",time.localtime()))),
		filemode='w')

def setLevel_(level):
	global g_loglevel
	g_loglevel = level

def logexc(e):
	logging.error("------ begin ------")
	logging.exception(e)
	logging.error("------  end  ------")
	
def logd(frame,msg):
	global g_loglevel
	if g_loglevel <= LOG_LEVEL_DEBUG: 
		logging.debug("["+frame.f_code.co_filename+"."+str(frame.f_lineno)+"]"+msg)

def logi(frame,msg):
	global g_loglevel
	if g_loglevel <= LOG_LEVEL_INFO:
		logging.info("["+frame.f_code.co_filename+"."+str(frame.f_lineno)+"]"+msg)
	
def logw(frame,msg):
	global g_loglevel
	if g_loglevel <= LOG_LEVEL_WARNING:
		logging.warning("["+frame.f_code.co_filename+"."+str(frame.f_lineno)+"]"+msg)
	
def loge(frame,msg):
	global g_loglevel
	if g_loglevel <= LOG_LEVEL_ERROR:
		logging.error("["+frame.f_code.co_filename+"."+str(frame.f_lineno)+"]"+msg)

initLog("server")
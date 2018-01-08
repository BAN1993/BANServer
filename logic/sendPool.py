import Queue
import logging

import player
import playerManager

msgQueus = {}
msgOutPuts = []

def delPlayer(conn):
	if conn in msgQueus:
		del msgQueus[conn]
	if conn in msgOutPuts:
		del msgOutPuts[conn]
	
def push(conn, data):
	if conn not in msgQueus:
		msgQueus[conn] = Queue.Queue()
	if conn not in msgOutPuts:
		msgOutPuts.append(conn)
		
	msgQueus[conn].put(data)
	
def getOutPuts():
	return msgOutPuts
	
def getMsg(conn):
	logging.debug("addr="+str(conn.getpeername()))
	try:
		return msgQueus[conn].get_nowait()
	except:
		if conn in msgOutPuts:
			msgOutPuts.remove(conn)
		raise
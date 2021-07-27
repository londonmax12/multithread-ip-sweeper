#! /bin/python3
import sys # System functions
import socket # Network Fuctions
import threading 
import multiprocessing
from datetime import datetime
import time
import pprint

openPorts = []
threads = {}

minPorts = 0
maxPorts = 0
totalPorts = 0

threadLoop = 0

currentPortsScanned = 0

scanning = True

# Define System Parameters
if len(sys.argv) == 5:
	minPorts = int(sys.argv[2])
	maxPorts = int(sys.argv[3])
	threadingRate = int(sys.argv[4])
	totalPorts = maxPorts - minPorts
	target = socket.gethostbyname(sys.argv[1]) # Translates a hostname into IPV4
	if maxPorts > 65535:
		print("Syntax Error: python3 ipSweeper.py <ip> <startPort(0-65536)> <endPort(0-65536> <threadingRate>")
	if minPorts < 0:
		print("Syntax Error: python3 ipSweeper.py <ip> <startPort(0-65536)> <endPort(0-65536)> <threadingRate>")
	if minPorts > maxPorts:
		print("Syntax Error: python3 ipSweeper.py <ip> <startPort(0-65536)> <endPort(0-65536)> <threadingRate>")
else:
	print("Syntax Error: python3 ipSweeper.py <ip> <startPort(0-65536)> <endPort(0-65535> <threadingRate>")
	sys.exit()

class ThreadClass(threading.Thread):
	def __init__(self, threadId):
		threading.Thread.__init__(self)
		self.threadId = threadId
	def run(self):
		try:
			checkPort(self.threadId)					
		except KeyboardInterrupt:
			print("\nExiting program.")
			sys.exit()

		except socket.gaierror:
			print("Hostname could not be resolved")
			sys.exit()
			
		except socket.error:
			print("Could not connect to server")			
			if(str(socket.error) == "<class 'OSError'>"):
				print("Try lowering the threading rate")
				sys.exit()
			print(socket.error)
			sys.exit()
#Checks if a port is open
def checkPort(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.setdefaulttimeout(1)
	result = s.connect_ex((target, port))
	print("Checking port {}".format(port))
	if result == 0:
		openPorts.append(port)
	global currentPortsScanned
	currentPortsScanned += 1
	s.close()

#Creates threads
def createThreads():
	try:
		if(threadingRate < totalPorts - currentPortsScanned):
			for thread in range(currentPortsScanned, threadingRate * threadLoop):
				threads["thread{0}".format(thread)] = ThreadClass(thread)
			for thread in range(currentPortsScanned, threadingRate * threadLoop):
				threads["thread{0}".format(thread)].start()
			for thread in range(currentPortsScanned, threadingRate * threadLoop):
				threads["thread{0}".format(thread)].join()	
			addToLoop()
		elif(totalPorts - currentPortsScanned > 0):
			for thread in range(currentPortsScanned, totalPorts + 1):
				threads["thread{0}".format(thread)] = ThreadClass(thread)
			for thread in range(currentPortsScanned, totalPorts + 1):
				threads["thread{0}".format(thread)].start()
			for thread in range(currentPortsScanned, totalPorts + 1):
				threads["thread{0}".format(thread)].join()						
	except KeyboardInterrupt:
		
		sys.exit()	
def addToLoop():
	if(threading.active_count() == 1):
		global threadLoop
		threadLoop += 1
		createThreads()

				
print("=" * 55)
print("IP SWEEP")
print("Scanning target " +target)
print("Time started:" +str(datetime.now()))
print("Threading rate:" +str(threadingRate))
print("=" * 55)

print("\nThreading...")
t0 = time.time()
addToLoop()
t1 = time.time()

print("=" * 55)
print("Results:")
print("\nTime elapsed:{} seconds".format(round(t1 - t0, 2)))
print("Open ports found ({}):".format(len(openPorts)))
if len(openPorts) > 0:
	print(openPorts)
else:
	print("None")
print("=" * 55)
	
sys.exit()

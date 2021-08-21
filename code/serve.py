from threading import Thread 
import random
import socket
import utils
import json
import time 
import sys 
import os 


def create_listener(port):
	maxtries = 3; created = False
	s = []
	while maxtries > 0 and not created:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(('0.0.0.0', port))
			s.listen(5)
			created = True
		except socket.error:
			time.sleep(5)
			pass
		maxtries -= 1
	if not created:
		exit()
	return s

def client_handler(csock, caddr, logfile):
	# Get their request
	request = ''; t0 = time.time()
	waiting = True; timeout = 3.0
	try:
		while waiting and (time.time() - t0) < timeout:
			request = csock.recv(1024).decode('utf-8')
			waiting = False
	except socket.error:
		print('[!!] Unable to get request from %s' % caddr[0])
		waiting = False
		pass
	# Maybe send something silly
	if not waiting:
		try:
			csock.send(open('page.html','r').read().encode('utf-8'))
		except socket.error:
			pass
	# Log Everything 
	data = {'IP': caddr[0], 'Req': request}
	ld, lt = utils.create_timestamp()
	try:
		parsed = json.dumps(data)
	except:
		pass
		parsed = '{"%s" : "%s"' % (caddr[0], request)
	entry = ('Connection at %s - %s :\n'%(ld,lt)) +parsed+'\n'+'='*80+'\n'
	open('logs/'+logfile, 'a').write(entry)
	return True

class BasicTrap:
	served = []
	uptime = 0.0

	def __init__(self, p,useBot):
		if not os.path.isdir('logs'):
			os.mkdir('logs')
		self.inbound = p
		self.start = time.time()
		self.worker = Thread(target=self.run, args=())
		self.worker.setDaemon(True)
		self.worker.start()


	def run(self):
		running = True
		serve = create_listener(self.inbound)
		self.log = self.create_log()
		ld, lt = utils.create_timestamp()
		print('[*] Honeypot Started [%s - %s]' % (ld,lt))
		try:
			while running:
				c, ci = serve.accept()
				print('[*] \033[1m\033[31m%s:%d\033[0m has connected ' % (ci[0], ci[1]))
				handler = Thread(target=client_handler, args=(c, ci, self.log))
				handler.run()
				c.close()
		except KeyboardInterrupt:
			running = False 
			

	def create_log(self):
		ld,lt = utils.create_timestamp()
		fn = ld.replace('/', '-') + '_' + lt.replace(':','-')+'.log'
		if not os.path.isfile(fn):
			open('logs/web'+fn, 'w').write('Starting HoneyPot [%s - %s]\n' % (ld, lt))
		return  fn


def main():
	port = 8080
	if '-run' in sys.argv:
		os.system('python3 tripwire.py &')
		b = BasicTrap(port,useBot=True)
		b.run()

if __name__ == '__main__':
	main()

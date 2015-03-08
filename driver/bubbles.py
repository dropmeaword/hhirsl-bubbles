#!/usr/bin/env python
from itertools import cycle
from time import sleep

import optparse
import time
import threading
from OSC import *
from settings import *

__author__ = "Luis Rodil-Fernandez <root@derfunke.net>"
__version__ = "0.1a"


default_host_address = ("127.0.0.1", 2222)  # host, port tuple

class ShiftReg:
	""" Handle a shift register chip from RPi """
	def __init__(self, latch, clock, data):
		self.data_pin = data
		self.clock_pin = clock
		self.latch_pin = data

	def setup(self):
		self.write(self.data_pin, 0)
		self.write(self.clock_pin, 0)
		self.write(self.latch_pin, 0)

	def write(self, pin, value):
		pass
		#path = '/sys/class/gpio/gpio%d/value' % pin
		#with open(path, 'w') as f:
		#	f.write('1' if value else '0')

	def latch(self):
		self.write(self.latch_pin, 1)
		self.write(self.latch_pin, 0)

	def shift_bit(self, value):
		self.write(self.data_pin, value)
		self.write(self.clock_pin, 1)
		self.write(self.clock_pin, 0)


def read_lines(filename):
	with open(filename) as f:
		for line in f:
			yield line.strip()

def osc_handle_pattern(addr, tags, data, client_address):
	""" handle incoming OSC message """
	print("pattern received: {0}".format(data))
	pass

def main():
	# read command line options
	option_parser_class = optparse.OptionParser

	parser = option_parser_class(description='This program drives the network of actuators used in the work BUBBLES')

	parser.add_option('-v','--verbose', 
		action='store_true',
		dest="verbose",
		default=False, 
		help='verbose printing [default:%i]'% False)

	parser.add_option('-t','--test', 
		action='store_true',
		dest="testmode",
		default=False, 
		help='run in test mode [default:%i]'% False)

	parser.add_option('-s','--sequence', 
		action='store',
		type="string",
		dest="sequence_file",
		default="sequence.txt",
		help='name of the sequence file [default:%s]'% 'sequence.txt')

	parser.add_option('-i','--interval', 
		action='store',
		type=float,
		dest="interval",
		default=2,
		help='interval of time to wait between test frames [default:%s]'% 2)

	parser.add_option('-l','--listen-port', 
		type=int, 
		action='store',
		dest="listen_port",
		default=2222, 
		help='the port on which the driver will listen to OSC messages [default:%i]'% 2222 )

	(options,args) = parser.parse_args()

	s = None
	st = None
	try:
		if options.testmode:
			print("Test mode runs forever, press CTRL+C if you want to quit")
			# start execution
			sr = ShiftReg(latch = get_setting('latch_pin'), clock = get_setting('clock_pin'), data = get_setting('data_pin') )
			sr.setup()
			for frame in cycle(read_lines(options.sequence_file)):
				print("sending frame: {0}".format(frame))
				for pixel in frame:
					sr.shift_bit(pixel == '#')
				sr.latch()
				sleep(options.interval)
		else:
			host_address = (default_host_address[0], options.listen_port)
			print("Starting OSC server, listening on address {0}".format(host_address))
			s = OSCServer(host_address)
			s.addDefaultHandlers()
			s.addMsgHandler("/pattern", osc_handle_pattern)
			while True:
				s.handle_request()
				sleep(0.01)
	except KeyboardInterrupt, e:
		s.close()  # stop server thread if running
		print
		print "Roger that. Goodbye!"
		pass

if __name__ == '__main__':
	main()
	
#!/usr/bin/env python

import ConfigParser
import logging
from logging.handlers import RotatingFileHandler
from optparse import OptionParser
import os
import sys

from reader.snmp_address_reader import SnmpAddressReader
from writer.route53_address_writer import Route53AddressWriter

logger = logging.getLogger('beacon')

DEFAULT_CONFIG_FILENAME = 'beacon.cfg'

class BeaconError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Beacon(object):
	def __init__(self):
		self.reader = None
		self.writer = None
		# TODO: this can be improved
		self.rfc1918_addresses = [ '10.',
				'192.168.' ]

	def configure(self, config):
		self.reader = SnmpAddressReader()
		name = self.reader.__class__.__name__
		logger.debug("reader class = %s", name)
		if config.has_section(name):
			self.reader.configure(dict(config.items(name)))

		self.writer = Route53AddressWriter()
		name = self.writer.__class__.__name__
		logger.debug("writer class = %s", name)
		if config.has_section(name):
			self.writer.configure(dict(config.items(name)))

	def get_external_address(self):
		addresses = self.reader.get_addresses()
		for address in addresses:
			if address == "127.0.0.1":
				continue
			for a in self.rfc1918_addresses:
				if address.startswith(a):
					continue
			return address
		return None

	def run(self, argv):
		progname = os.path.basename(argv[0])
		cfgfilename = DEFAULT_CONFIG_FILENAME

		parser = OptionParser()
		parser.add_option("--verbose", "-v", dest="verbose",
				action="store_true", default=False)
		parser.add_option("-c", dest="cfgfilename", default=cfgfilename)
		options, args = parser.parse_args()
		argslength = len(args)

		logformat = '%(asctime)s %(levelname)-8s %(message)s'
		logging.basicConfig(format=progname + ": " + logformat)

		logging.getLogger().setLevel(logging.INFO)
		if options.verbose:
			logging.getLogger().setLevel(logging.DEBUG)

		config = ConfigParser.ConfigParser()
		try:
			config.readfp(open(cfgfilename))
		except IOError:
			sys.stderr.write("unable to open configuration: %s\n" % cfgfilename)
			return 2

		self.configure(config)

		address = self.get_external_address()
		logger.debug("address = %s", address)
		return 0

def add_logging_file_handler(filename, logformat, loglevel=logging.INFO):
	fileHandler = RotatingFileHandler(filename,
			maxBytes=10 * 1024 * 1024, backupCount=3)
	fileHandler.setFormatter(logging.Formatter(logformat))
	fileHandler.setLevel(loglevel)
	logging.getLogger().addHandler(fileHandler)
	return fileHandler

if __name__ == '__main__':
	beacon = Beacon()
	sys.exit(beacon.run(sys.argv))


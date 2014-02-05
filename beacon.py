#!/usr/bin/env python

import ConfigParser
import dns.resolver
from dns.resolver import NXDOMAIN
import logging
from logging.handlers import RotatingFileHandler
from optparse import OptionParser
import os
import sys

from reader.snmp_address_reader import SnmpAddressReader
from writer.route53_address_writer import Route53AddressWriter

logger = logging.getLogger('beacon')

DEFAULT_CONFIG_FILENAME = 'beacon.cfg'

class Beacon(object):
    def __init__(self):
        self.reader = None
        self.writer = None
        self.hostname = None
        # TODO: this can be improved
        self.rfc1918_addresses = ['10.',
                        '192.168.']

    def configure(self, config):
        name = 'main'
        if config.has_section(name):
            if config.has_option(name, 'hostname'):
                self.hostname = config.get(name, 'hostname')
                logger.debug("hostname = %s", self.hostname)

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

    def resolve_hostname(self):
        try:
            answers = dns.resolver.query(self.hostname, 'A')
            for rdata in answers:
                logger.info("current DNS record: %s", rdata)
        except NXDOMAIN:
            logger.info("DNS record not found")

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

        parser = OptionParser()
        parser.add_option("--verbose", "-v", dest="verbose",
                        action="store_true", default=False)
        parser.add_option("-c", dest="cfgfilename",
                        default=DEFAULT_CONFIG_FILENAME)
        parser.add_option("-l", dest="logfilename")
        options, args = parser.parse_args()
        #argslength = len(args)

        logformat = '%(asctime)s %(levelname)-8s %(message)s'
        if options.logfilename:
            add_logging_file_handler(options.logfilename, logformat,
                    logging.DEBUG)
        else:
            logging.basicConfig(format=progname + ": " + logformat)

        logging.getLogger().setLevel(logging.INFO)
        if options.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        cfgfilename = options.cfgfilename
        config = ConfigParser.ConfigParser()
        try:
            config.readfp(open(cfgfilename))
        except IOError:
            sys.stderr.write("unable to open configuration: %s\n" % cfgfilename)
            return 2

        self.configure(config)

        self.resolve_hostname()

        address = self.get_external_address()
        logger.debug("address = %s", address)

        self.writer.update_addresses(self.hostname, [address])

        return 0

def add_logging_file_handler(filename, logformat, loglevel=logging.INFO):
    file_handler = RotatingFileHandler(filename,
                    maxBytes=10 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(logging.Formatter(logformat))
    file_handler.setLevel(loglevel)
    logging.getLogger().addHandler(file_handler)
    return file_handler

if __name__ == '__main__':
    n = 0
    try:
        beacon = Beacon()
        n = beacon.run(sys.argv)
    except:
        logger.exception("unexpected error")
        n = 1
    sys.exit(n)


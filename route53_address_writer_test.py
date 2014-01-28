import ConfigParser
import unittest

from route53_address_writer import Route53AddressWriter

class Route53AddressWriterTest(unittest.TestCase):

	def setUp(self):
		self.writer = Route53AddressWriter()

		config = ConfigParser.ConfigParser()
		config.readfp(open('beacon.cfg'))
		self.writer.configure(dict(config.items('Route53AddressWriter')))

	def test_update_addresses(self):
		self.writer.update_addresses([])

if __name__ == '__main__':
	unittest.main()


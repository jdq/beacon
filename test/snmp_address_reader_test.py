import ConfigParser
import unittest

from reader.snmp_address_reader import SnmpAddressReader

class SnmpAddressReaderTest(unittest.TestCase):

	def setUp(self):
		self.reader = SnmpAddressReader()

		config = ConfigParser.ConfigParser()
		config.readfp(open('beacon.cfg'))
		self.reader.configure(dict(config.items('SnmpAddressReader')))

	def test_get_addresses(self):
		addresses = self.reader.get_addresses()
		self.assertTrue(len(addresses) > 0)

if __name__ == '__main__':
	unittest.main()


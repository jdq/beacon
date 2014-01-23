import unittest

from snmp_address_reader import SnmpAddressReader

class SnmpAddressReaderTest(unittest.TestCase):

	def setUp(self):
		self.reader = SnmpAddressReader()
		self.reader.host = '192.168.100.1'

	def test_get_addresses(self):
		addresses = self.reader.get_addresses()
		self.assertTrue(len(addresses) > 0)

if __name__ == '__main__':
	unittest.main()


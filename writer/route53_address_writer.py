import logging
import route53

from writer.address_writer import AddressWriter

logger = logging.getLogger('Route53Writer')

class Route53AddressWriter(AddressWriter):
	def __init__(self):
		self.aws_access_key_id = None
		self.aws_secret_access_key = None
		self.zone_id = None

	def configure(self, dict):
		if 'access_key_id' in dict:
			self.aws_access_key_id = dict['access_key_id']
		if 'secret_access_key' in dict:
			self.aws_secret_access_key = dict['secret_access_key'] 
		if 'zone_id' in dict:
			self.zone_id = dict['zone_id'] 

	def update_addresses(self, addresses):
		conn = route53.connect(
			aws_access_key_id = self.aws_access_key_id,
			aws_secret_access_key = self.aws_secret_access_key
		)
		zone = conn.get_hosted_zone_by_id(self.zone_id)
		logger.debug("retrieved zone %s" % zone.name)
		print(zone.name) # XXX


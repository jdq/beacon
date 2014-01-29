import abc

class AddressWriter(object):
	__metaclass__ = abc.ABCMeta
	def configure(self, dict):
		pass
	@abc.abstractmethod
	def update_addresses(self, addresses):
		pass


import abc


class AddressWriter(object):
    __metaclass__ = abc.ABCMeta

    def configure(self, dictionary):
        pass

    @abc.abstractmethod
    def update_addresses(self, hostname, addresses):
        pass

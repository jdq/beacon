import abc


class AddressReader(object):
    __metaclass__ = abc.ABCMeta

    def configure(self, dictionary):
        pass

    @abc.abstractmethod
    def get_addresses(self):
        return []

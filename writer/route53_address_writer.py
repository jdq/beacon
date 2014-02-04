import logging
import route53

from writer.address_writer import AddressWriter

logger = logging.getLogger('Route53Writer')

class Route53AddressWriter(AddressWriter):
    def __init__(self):
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.zone_id = None
        self.conn = None

    def configure(self, dictionary):
        if 'access_key_id' in dictionary:
            self.aws_access_key_id = dictionary['access_key_id']
        if 'secret_access_key' in dictionary:
            self.aws_secret_access_key = dictionary['secret_access_key']
        if 'zone_id' in dictionary:
            self.zone_id = dictionary['zone_id']
            logger.debug("aws zone id = %s", self.zone_id)

        self.conn = route53.connect(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
        )

    def get_record_set(self, name):
        zone = self.conn.get_hosted_zone_by_id(self.zone_id)
        logger.debug("retrieved zone %s", zone.name)
        for record_set in zone.record_sets:
            logger.debug("record set = %s", record_set.name)
            if record_set.name == name:
                logger.debug("matched record set = %s", record_set)
                return record_set
        logger.error("name not found in zone")
        return None

    def update_addresses(self, hostname, addresses):
        record_set = self.get_record_set(hostname)
        if not record_set:
            pass # XXX
        logger.debug("record set values = %s", record_set.records)
        if set(record_set.records) == set(addresses):
            logger.info("no update required")
        else:
            logger.info("updating record set")
            record_set.records = addresses
            record_set.save()


import logging
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1902 import IpAddress

from beacon import AddressReader

logger = logging.getLogger('SnmpAddressReader')

class SnmpAddressReader(AddressReader):

    def __init__(self):
        self.host = 'localhost'
        self.port = 161
        self.password = 'public'

    def get_addresses(self):
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(self.password),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            1, 25,
            cmdgen.MibVariable('IP-MIB', 'ipAdEntAddr'),
            lookupNames=True, lookupValues=True, maxRows=20
        )

        results = []
        if errorIndication:
            logger.error('%s' % errorIndication)
        else:
            if errorStatus:
                logger.error('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex) - 1] or '?'
                )
            )
            else:
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        if isinstance(val, IpAddress):
                            logger.debug('%s = %s' % (name.prettyPrint(),
                                    val.prettyPrint()))
                            results.append(val.prettyPrint())
        return results


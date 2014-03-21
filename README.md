
Beacon is a Python utility to update DNS.  It currently reads an address
from a SNMP node and updates an Amazon Route53 record.  Beacon is
designed to be extensible by employing a reader and writer for DNS
records.  For example, a reader may obtain the current address from
an online service such as Google and a writer may send a dynamic DNS
update as specified by RFC 2136.

http://aws.amazon.com/route53/
https://www.google.com/#q=what+is+my+ip
https://tools.ietf.org/html/rfc2136


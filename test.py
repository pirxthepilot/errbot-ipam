from phpipam import PhpIpam
from ConfigParser import SafeConfigParser
import json
import os

# Config file
cwd = os.path.dirname(os.path.realpath(__file__))
config = SafeConfigParser()
config.read(os.path.join(cwd, 'config.ini'))

# Config variables
ipam_baseurl = config.get('phpipam', 'baseurl')
ipam_id = config.get('phpipam', 'id')
ipam_user = config.get('phpipam', 'user')
ipam_pw = config.get('phpipam', 'password')
ipam_sectionid = config.get('phpipam', 'sectionid')
if config.has_option('phpipam', 'ca_cert'):
    ca_cert = config.get('phpipam', 'ca_cert')
else:
    ca_cert = None

ipaddress = '192.168.150.224'


ipam_sess = PhpIpam(ipam_baseurl, ipam_id, ipam_user, ipam_pw, ca_cert)
ipam_sess.connect()
query = {}
query = ipam_sess.get_address_info(ipaddress)
#query = ipam_sess.get_subnet_info(ipaddress)
#query = json.loads(ipam_sess.get_addresses(ipaddress))['data']
#query.update(json.loads(ipam_sess.get_subnet_info(ipaddress))['data'])
#query.update(json.loads(ipam_sess.get_subnet_usage(ipaddress))['data'])
#query.update(json.loads(ipam_sess.get_subnet_firstfree(ipaddress))['data'])
if query:
    #print json.dumps(json.loads(query), indent=4)
    print json.dumps(query, indent=4)
ipam_sess.close()

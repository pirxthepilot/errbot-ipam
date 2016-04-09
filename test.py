from phpipam import PhpIpam
import json

# Vars
ipam_baseurl = 'http://localhost:8080'
ipam_id = 'botbot'
ipam_user = 'errbot'
ipam_pw = 'oopsie123'
ipaddress = '10.10.1.0/24'


ipam_sess = PhpIpam(ipam_baseurl, ipam_id, ipam_user, ipam_pw)
ipam_sess.connect()
query = {}
#query = ipam_sess.get_address_info(ipaddress)
#query = ipam_sess.get_subnet_info(ipaddress)
#query = json.loads(ipam_sess.get_addresses(ipaddress))['data']
query.update(json.loads(ipam_sess.get_subnet_info(ipaddress))['data'])
query.update(json.loads(ipam_sess.get_subnet_usage(ipaddress))['data'])
query.update(json.loads(ipam_sess.get_subnet_firstfree(ipaddress))['data'])
if query:
    #print json.dumps(json.loads(query), indent=4)
    print json.dumps(query, indent=4)
ipam_sess.close()

from errbot import BotPlugin, botcmd
from errbot.rendering import text
from phpipam import PhpIpam
from ConfigParser import SafeConfigParser
import json
import re
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


class Ipam(BotPlugin):
    """phpipam plugin for Errbot"""

    @botcmd
    def ipam(self, msg, address):
        """Query IPAM for IP or network address"""
        ipam_sess = PhpIpam(ipam_baseurl, ipam_id, ipam_user, ipam_pw, ca_cert)
        ipam_sess.connect()
        netaddr_re = re.compile("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\/[0-9]+")

        # Subnet query
        if netaddr_re.match(address):
            info = ipam_sess.get_subnet_info(address)
            usage = ipam_sess.get_subnet_usage(address)
            first = ipam_sess.get_subnet_firstfree(address)
            query = {}
            if info and usage and first:
                query.update(json.loads(info)['data'])
                query.update(json.loads(usage)['data'])
                query.update(json.loads(first)['data'])
                return self.output_subnet(query)
            else:
                return "IPAM says: No result or query error"

        # IP address query
        else:
            query = ipam_sess.get_address_info(address)
            if query:
                return self.output_ip(json.loads(query)['data'][0])
            else:
                return "IPAM says: No result or invalid query"

        ipam_sess.close()

    def output_ip(self, data):
        url = ("%s/?page=subnets&section=%s"
               "&subnetId=%s&sPage=address-details&ipaddrid=%s"
               % (ipam_baseurl, ipam_sectionid, data['subnetId'], data['id']))
        message = ("IPAM says:\n"
                   " ========== \n"
                   "[ip address] %s\n"
                   "[hostname] %s\n"
                   "[description] %s\n"
                   "[link] %s\n"
                   " ========== \n"
                   % (data['ip'],
                      data['hostname'],
                      data['description'],
                      url))
        md = text()
        return md.convert(message)

    def output_subnet(self, data):
        url = ("%s/?page=subnets&section=%s&subnetId=%s"
               % (ipam_baseurl, data['sectionId'], data['id']))
        message = ("IPAM says:\n"
                   " ========== \n"
                   "[subnet] %s/%s\n"
                   "[description] %s\n"
                   "[used] %s/%s\n"
                   "[first free ip] %s\n"
                   "[link] %s\n"
                   " ========== \n"
                   % (data['subnet'],
                      data['mask'],
                      data['description'],
                      data['used'],
                      data['maxhosts'],
                      data['first_free'],
                      url))
        md = text()
        return md.convert(message)

from errbot import BotPlugin, botcmd
from errbot.rendering import text
from phpipam import PhpIpam
import json

# Vars
ipam_baseurl = 'http://localhost:8080'
ipam_id = 'botbot'
ipam_user = 'errbot'
ipam_pw = 'oopsie123'


class Ipam(BotPlugin):
    """phpipam plugin for Errbot"""

    @botcmd
    def ipam(self, msg, ipaddress):
        """Check IPAM for IP Address"""
        ipam_sess = PhpIpam(ipam_baseurl, ipam_id, ipam_user, ipam_pw)
        ipam_sess.connect()
        query = ipam_sess.get_address_info(ipaddress)
        ipam_sess.close()
        if query:
            return self.output(json.loads(query)['data'][0])
        else:
            return "IP address not found."

    def output(self, data):
        message = ("IPAM says:\n"
                   " ========== \n"
                   "[ip address] %s\n"
                   "[hostname] %s\n"
                   "[description] %s\n"
                   " ========== \n"
                   % (data['ip'],
                      data['hostname'],
                      data['description']))
        md = text()
        return md.convert(message)

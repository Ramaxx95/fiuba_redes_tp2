
from pox.core import core as core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''
from pox.lib.addresses import IPAddr
log = core.getLogger
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ['HOME']

''' Add your global variables here ... '''
IPV4_TYPE = 0x0800
TCP_PROTO_NUMBER = 6
UDP_PROTO_NUMBER = 17

class Firewall (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        # Se define lista de bloqueados por firewall
        blocked = [
            (80, None, None, None), # Bloquea todos los mensajes entrantes al puerto 80
            (5001, UDP_PROTO_NUMBER, '10.0.0.1', None), # Bloquea todos los mensajes UDP provenientes del host 1 al puerto 5001
            (None, None, '10.0.0.2', '10.0.0.3'), # Bloquea todos los mensajes del host 2 al 3
            (None, None, '10.0.0.3', '10.0.0.2') # Bloquea todos los mensajes del host 3 al 2
        ]

        for port, protocol, src_host, dest_host in blocked:
            match = of.ofp_match(dl_type=IPV4_TYPE)

            if port:
                match.tp_dst = port
            
            if protocol:
                match.nw_proto = protocol

            if src_host:
                match.nw_src = IPAddr(src_host)

            if dest_host:
                match.nw_dst = IPAddr(dest_host)

            message = of.ofp_flow_mod()
            message.match = match
            # Drops packet by sending it to OFPP_NONE 
            message.actions.append(of.ofp_action_output(port=of.OFPP_NONE))
            message.priority = 100

            event.connection.send(message)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))


def launch():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)

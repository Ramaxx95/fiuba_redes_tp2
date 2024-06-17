
from pox.core import core as core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
import os

from pox.lib.addresses import IPAddr
log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ['HOME']


IPV4_TYPE = 0x0800
TCP_PROTO_NUMBER = 6
UDP_PROTO_NUMBER = 17


class Firewall (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        # Se define lista de bloqueados por firewall
        log.debug("[DEBUG] Switch %s has been connected", dpidToStr(event.dpid))

        # Quita paquetes TCP/IPv4 que vayan al puerto 80
        event.connection.send(of.ofp_flow_mod(priority=42,
                                              match=of.ofp_match(nw_proto=TCP_PROTO_NUMBER,
                                                                 dl_type=IPV4_TYPE,
                                                                 tp_dst=80)))

        # Quita paquetes UDP/IPv4 que vayan al puerto 80
        event.connection.send(of.ofp_flow_mod(priority=42,
                                              match=of.ofp_match(nw_proto=UDP_PROTO_NUMBER,
                                                                 dl_type=IPV4_TYPE,
                                                                 tp_dst=80)))

        # Quita paquetes UDP con puerto destino 5001 proveninetes del host 1
        event.connection.send(of.ofp_flow_mod(priority=42,
                                              match=of.ofp_match(nw_proto=UDP_PROTO_NUMBER,
                                                                 dl_type=IPV4_TYPE,
                                                                 nw_src=IPAddr('10.0.0.1'),
                                                                 tp_dst=5001)))

        # Los hosts 2 y 3 no pueden comunicarse de ninguna manera
        event.connection.send(of.ofp_flow_mod(priority=42,
                                              match=of.ofp_match(nw_proto=TCP_PROTO_NUMBER,
                                                                 dl_type=IPV4_TYPE,
                                                                 nw_src=IPAddr('10.0.0.2'),
                                                                 nw_dst=IPAddr('10.0.0.3'))))

        event.connection.send(of.ofp_flow_mod(priority=42,
                                              match=of.ofp_match(nw_proto=TCP_PROTO_NUMBER,
                                                                 dl_type=IPV4_TYPE,
                                                                 nw_src=IPAddr('10.0.0.3'),
                                                                 nw_dst=IPAddr('10.0.0.2'))))

        log.debug("[DEBUG] Firewall rules installed on %s", dpidToStr(event.dpid))


def launch():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)

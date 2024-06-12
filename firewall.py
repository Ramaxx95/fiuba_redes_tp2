
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ['HOME']

''' Add your global variables here ... '''
IPV4_TYPE = 0x0800
TCP_PROTO_NUMBER = 6

class Firewall (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self, event):
        match = of.ofp_match(tp_dst = 80, dl_type=IPV4_TYPE, nw_proto=TCP_PROTO_NUMBER)

        message = of.ofp_flow_mod()
        message.match = match
        # Drops packet by sending it to OFPP_NONE
        message.actions.append(of.ofp_action_output(port=of.OFPP_NONE))
        message.priority = 10

        event.connection.send(message)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))


def launch():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)


launch()
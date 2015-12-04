from mininet.node import Node
from mininet.link import Link
from mininet.log import setLogLevel, info
from mininet.util import quietRun
from mininet.topo import Topo

import subprocess

from time import sleep


class DefaultNetwork(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)
        setLogLevel('info')
        """Create the surfnet test topology from scratch"""
        CONTROLLER_IP = '192.168.1.60'
        DEFAULT_IP = '192.168.1.30'
        info('*** Cleaning any bridges and interfaces already present')
        subprocess.call("clean-ifaces.sh", shell=True)

        info('*** Creating Nodes\n')
        controller = self.addNode('opendaylight', inNamespace=False)
        pe1 = self.addSwitch('PE1')
        pe2 = self.addSwitch('PE2')
        pe3 = self.addSwitch('PE3')
        p1 = self.addSwitch('P1')
        p2 = self.addSwitch('P2')
        net1 = self.addHost('net1')
        #net1.cmd('py net1.setIP(\'192.168.200.2/24\')')
        #net1.setIP(net1-eth0, '192.168.200.2', 24)
        self.g.node['net1'].setIP(net1-eth0, '192.168.200.2', 24)
        net2 = self.addHost('net2')
        #net2.cmd('py net2.setIP(\'192.168.250.2/24\')')
        #net2.setIP(net2-eth0, '192.168.250.2', 24)
        info('*** Creating links\n')

        # PE1:1
        self.addLink(net1, pe1, intfName2='PE1-eth0',
                     params2={'ip': '192.168.200.1/24'})
        # PE1:2
        self.addLink(p1, pe1)

        # P1 <-->  P2
        self.addLink(p1, p2)
        # PE2 <--> P2
        self.addLink(pe2, p2)
        # PE3 <--> P2
        self.addLink(pe3, p2)

        # Net2 --> PE2
        self.addLink(net2, pe2, intfName2='PE2-eth2',
                     params2={'ip': '192.168.250.1/24'})

class LinuxRouter(Node):
    """A Node with IP forwarding enabled."""
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self ):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

topos = {'mytopo': (lambda: DefaultNetwork())}


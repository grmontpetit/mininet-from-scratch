from mininet.net import Mininet
from mininet.node import Node
from mininet.link import Link
from mininet.log import setLogLevel, info
from mininet.util import quietRun
from mininet.cli import CLI

import subprocess

from time import sleep


def default_network(cname='controller', cargs='-v ptcp:' ):
    """Create the surfnet test topology from scratch"""
    CONTROLLER_IP = '192.168.1.135'
    DEFAULT_IP = '192.168.1.30'
    info('*** Cleaning any bridges and interfaces already present')
    subprocess.call("clean-ifaces.sh", shell=True)

    info('*** Creating Nodes\n')
    controller = Node('opendaylight', inNamespace=False)
    pe1 = Node('PE1', cls=LinuxRouter)
    pe2 = Node('PE2', cls=LinuxRouter)
    pe3 = Node('PE3', cls=LinuxRouter)
    p1 = Node('P1', cls=LinuxRouter)
    p2 = Node('P2', cls=LinuxRouter)
    net1 = Node('net1')
    net2 = Node('net2')

    info('*** Creating links\n')

    # PE1:1
    Link(net1, pe1, intfName2='PE1-eth0',
         params2={'ip': '192.168.200.1/24'})
    # PE1:2
    Link(p1, pe1)

    # P1 <-->  P2
    Link(p1, p2)
    # PE2 <--> P2
    Link(pe2, p2)
    # PE3 <--> P2
    Link(pe3, p2)

    # Net2 --> PE2
    Link(net2, pe2, intfName2='PE2-eth2',
         params2={'ip': '192.168.250.1/24'})

    info("*** Configuring hosts\n")
    net1.setIP('192.168.200.2/24')
    net2.setIP('192.168.250.2/24')
    info(str(net1) + '\n')
    info(str(net2) + '\n')

    info("*** Starting network using Open vSwitch\n")
    controller.cmd(cname + ' ' + cargs + '&')
    pe1.cmd('ovs-vsctl del-br br0')
    pe1.cmd('ovs-vsctl add-br br0')
    pe2.cmd('ovs-vsctl del-br br1')
    pe2.cmd('ovs-vsctl add-br br1')
    pe3.cmd('ovs-vsctl del-br br2')
    pe3.cmd('ovs-vsctl add-br br2')
    p1.cmd('ovs-vsctl del-br br3')
    p1.cmd('ovs-vsctl add-br br3')
    p2.cmd('ovs-vsctl del-br br4')
    p2.cmd('ovs-vsctl add-br br4')
    for intf in pe1.intfs.values():
        print pe1.cmd('ovs-vsctl add-port br0 %s' % intf)
    for intf in pe2.intfs.values():
        print pe2.cmd('ovs-vsctl add-port br1 %s' % intf)
    for intf in pe3.intfs.values():
        print pe3.cmd('ovs-vsctl add-port br2 %s' % intf)
    for intf in p1.intfs.values():
        print p1.cmd('ovs-vsctl add-port br3 %s' % intf)
    for intf in p2.intfs.values():
        print p2.cmd('ovs-vsctl add-port br4 %s' % intf)

    info('*** Setting controller on all the switches\n')
    pe1.cmd('ovs-vsctl set-controller br0 tcp:'+CONTROLLER_IP+':6633')
    pe2.cmd('ovs-vsctl set-controller br1 tcp:'+CONTROLLER_IP+':6633')
    pe3.cmd('ovs-vsctl set-controller br2 tcp:'+CONTROLLER_IP+':6633')
    p1.cmd('ovs-vsctl set-controller br3 tcp:'+CONTROLLER_IP+':6633')
    p2.cmd('ovs-vsctl set-controller br4 tcp:'+CONTROLLER_IP+':6633')

    info( '*** Waiting for switch to connect to controller' )
    while 'is_connected' not in quietRun( 'ovs-vsctl show' ):
        sleep( 1 )
        info( '.' )
    info( '\n' )


class LinuxRouter(Node):
    """A Node with IP forwarding enabled."""

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self ):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

def run():
    """Mininet from scratch"""
    #Mininet.init()
    topo = default_network()
    net = Mininet(topo=topo)  # controller is used by s1-s3
    net.start()
    info('*** Routing Table on Router:\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
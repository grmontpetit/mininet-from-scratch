from mininet.node import Node
from mininet.link import Link
from mininet.log import setLogLevel, info

def default_network():
    """Create the surfnet test topology from scratch"""
    info('*** Creating Nodes\n')
    controller = Node('opendaylight', inNamespace=False)
    pe1 = Node('PE1', inNamespace=False)
    pe2 = Node('PE2', inNamespace=False)
    pe3 = Node('PE3', inNamespace=False)
    p1 = Node('P1', inNamespace=False)
    p2 = Node('P2', inNamespace=False)
    net1 = Node('net1')
    net2 = Node('net2')

    info('*** Creating links\n')
    Link(pe1, p1)
    Link(p1, p2)
    Link(p2, pe2)
    Link(p2, pe3)
    Link(net1, pe1)
    Link(net2, pe2)

    info( "*** Configuring hosts\n" )
    net1.setIP('192.168.200.2/24')
    net2.setIP('192.168.250.2/24')
    info(str(net1) + '\n')
    info(str(net2) + '\n')

    info( "*** Starting network using Open vSwitch\n" )

if __name__ == '__main__':
    setLogLevel( 'info' )
    default_network()
    #topos = { 'mytopo': ( lambda: MyTopo() ) }
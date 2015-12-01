from mininet.net import Mininet
from mininet.topo import LinearTopo
from mininet.node import Node
from mininet.log import setLogLevel, info

#tree4 = TreeTopo(depth=2,fanout=2)
#net = Mininet(topo=tree4)
#net.start()
#h1, h4  = net.hosts[0], net.hosts[3]
#print h1.cmd('ping -c1 %s' % h4.IP())
#net.stop()

def emptyNet():
    # Create a linear topology with 4 switches with 1 host per switches
    linear = LinearTopo(k=4, n=1)
#    net = Mininet(controller=remote_controller,
#                  switch=OVSKernelSwitch, link=TCLink)
    net = Mininet(topo=linear)
    controller = net.addController('opendaylight',
                                   controller=remote_controller,
                                   # replace this IP with the IP on your network
                                   ip="192.168.1.60",
                                   port=6633)

    h1 = net.addHost( 'h1' )
    h2 = net.addHost( 'h2' )

    s1 = net.addSwitch( 's1' , mac='00:00:00:00:00:01' )
    s2 = net.addSwitch( 's2' , mac='00:00:00:00:00:02' )

    net.addLink('s1','s2')
    net.addLink('s2','s1')

    net.addLink('s1','h1')
    net.addLink('s2','h2')


    s1.start(c1)
    s2.start(c1)
    s3.start(c1)
    net.start()
    net.staticArp()
    CLI( net )
    net.stop()
 if __name__ == '__main__':
  setLogLevel( 'info' )
  emptyNet()
topos = { 'mytopo': ( lambda: MyTopo() ) }

def surfnet():
    """Create the surfnet test topology from scratch"""
    info('Creating Nodes\n'')
    controller = Node('opendaylight', inNamespace=False)
    pe1 = Node('PE1', inNamespace=False)
    pe2 = Node('PE2', inNamespace=False)
    pe3 = Node('PE3', inNamespace=False)
    p1 = Node('P1', inNamespace=False)
    p2 = Node('P2', inNamespace=False)

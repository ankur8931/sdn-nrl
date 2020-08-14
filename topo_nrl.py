from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.topo import Topo

setLogLevel( 'info' )

# Two local and one "external" controller (which is actually c0)
# Ignore the warning message that the remote isn't (yet) running
c0 = RemoteController( 'c0', ip='127.0.0.1', port=6654 )
c1 = RemoteController( 'c1', ip='127.0.0.1', port=6655 )

cmap = { 's1': c0, 's2':c0, 's3': c1}

class MultiSwitch( OVSSwitch ):
    "Custom Switch() subclass that connects to different controllers"
    def start( self, controllers ):
        return OVSSwitch.start( self, [ cmap[ self.name ] ] )

class MyTopo( Topo ):
    "Simple topology example."

    def build(self):

        # Initialize topology
#adding hosts
        s1_h1 = self.addHost('h1')
        s1_h2 = self.addHost('h2')
        s2_h3 = self.addHost('h3')
        s3_h4 = self.addHost('h4')
        s3_h5 = self.addHost('h5')
        #adding switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        #adding links
        self.addLink(s1_h1, s1)
        self.addLink(s1_h2, s1)
        self.addLink(s2_h3, s2)
        self.addLink(s3_h4, s3)
        self.addLink(s3_h5, s3)
        self.addLink(s1,s2)
        self.addLink(s2,s3)
        #self.addLink(s1,s3)

topo = MyTopo() 
net = Mininet( topo=topo, switch=MultiSwitch, build=False )
for c in [c0, c1 ]:
    net.addController(c)

#net.build()
net.start()
CLI( net )
net.stop()

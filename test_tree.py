# DataBlast Demo Mininet by Andre
# Tree Topology (fanout = k)
#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import UserSwitch, OVSKernelSwitch, RemoteController
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.clean import cleanup
from mininet.cli import CLI
from time import sleep
from random import randint

class treebw(Topo):
    def __init__(self, linkopts1, linkopts2,linkopts3,fanout, **opts):
        Topo.__init__(self, **opts)
        self.linkopts1 = linkopts1
        self.linkopts2 = linkopts2
        self.linkopts3 = linkopts3
        self.fanout = fanout
        s=[]
        h=[]
        l=[1]
        a=0
        c=0
        for i in irange(1,1+fanout+fanout**2):
            switch = self.addSwitch('s%s' % i)
            s.append(switch)
        for i in irange(1,fanout**3):
            host = self.addHost('h%s' % i)
            h.append(host)
        for i in range(fanout-1):
            a=a+fanout+1
            l.append(a+1)
        for i in l:
            link = self.addLink(s[0], s[i],**linkopts1)
        for i in l:
            b=0
            for j in irange(1,fanout):
                link = self.addLink(s[i],s[b+i+1],**linkopts2)
                for k in irange(1,fanout):
                    link = self.addLink(h[c],s[b+i+1],**linkopts3)
                    c=c+1
                b=b+1
                   
def pingTest():        
    linkopts1 = {'bw':5, 'delay':'5ms'}
    linkopts2 = {'bw':3, 'delay':'10ms'}
    linkopts3 = {'bw':1, 'delay':'15ms'}
    topo = treebw(linkopts1, linkopts2, linkopts3, fanout=3)    
    net = Mininet(topo=topo, switch=OVSKernelSwitch , link=TCLink,controller=RemoteController) 
    net.start()
    hosts=net.hosts
    for i in range(len(hosts)):
        for j in range(len(hosts)):
            if i != j:
                hosts[i].cmd( 'ping -c5', hosts[j].IP())
                sleep(randint(1,3))

    net.stop()  
   
if __name__ == '__main__':
   setLogLevel('info')
   pingTest()
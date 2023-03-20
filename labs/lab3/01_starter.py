### Distance vector routing
import random,sys,math
from optparse import OptionParser
from p3_netsim import *
import p3_tests
import os
import time

class DVRouter(Router):
    INFINITY = 32

    def send_advertisement(self, time):
        adv = self.make_dv_advertisement()
        for link in self.links:
            p = self.network.make_packet(self.address, self.peer(link), 
                                         'ADVERT', time,
                                         color='red', ad=adv)
            link.send(self, p)        
            
    # Make a distance vector protocol advertisement, which will be sent
    # by the caller along all the links
    def make_dv_advertisement(self):
        ## Task 3.1
        ## Your code here
        pass

    def link_failed(self, link):
        # If a link is broken, remove it from my routing/cost table
        self.clear_routes(self) 
        
    def process_advertisement(self, p, link, time):
        self.integrate(link, p.properties['ad'])

    # Integrate new routing advertisement to update routing
    # table and costs
    def integrate(self,link,adv):
        ## Task 3.2
        ## Your code here 
        pass

# A network with nodes of type DVRouter.
class DVRouterNetwork(RouterNetwork):
    # nodes should be an instance of DVNode (defined above)
    def make_node(self,loc,address=None):
        return DVRouter(loc,address=address)

########################################################################

if __name__ == '__main__':
    
    gui = True
    numnodes = 12
    simtime = 2000
    rand = False

    if rand == True:
        rg = RandomGraph(numnodes)
        (NODES, LINKS) = rg.genGraph()
    else:
        # build the deterministic test network
        #   A---B   C---D
        #   |   | / | / |
        #   E   F---G---H
        # format: (name of node, x coord, y coord)

        NODES =(('A',0,0), ('B',1,0), ('C',2,0), ('D',3,0),
                ('E',0,1), ('F',1,1), ('G',2,1), ('H',3,1))

        # format: (link start, link end)
        LINKS = (('A','B'),('A','E'),('B','F'),('E','F'),
                 ('C','D'),('C','F'),('C','G'),
                 ('D','G'),('D','H'),('F','G'),('G','H'))

    # setup graphical simulation interface
    if gui == True:
        net = DVRouterNetwork(simtime, NODES, LINKS, 0)
        sim = NetSim()
        sim.SetNetwork(net)
        sim.MainLoop()
    else:
        p3_tests.verify_routes(DVRouterNetwork)
    time.sleep(3)
    os._exit(0)
        

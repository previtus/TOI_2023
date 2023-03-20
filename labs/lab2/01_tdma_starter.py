#Time Division Multiple Access (TDMA)
import os
import random, sys, wx, math, time
from optparse import OptionParser
from p2_wsim import *
import matplotlib.pyplot as p

###############################################################

class TDMANode(WirelessNode):
    def __init__(self, location, network, retry):
        WirelessNode.__init__(self, location, network, retry)
        # any additional state or variables may be set here

    def channel_access(self, time, ptime, numnodes):
        ## Task 3.1
        ## TODO: control channel access
        pass

    def on_collision(self, packet):
        pass

    def on_xmit_success(self, packet):
        pass

################################################################

class TDMAWirelessNetwork(WirelessNetwork):
    def __init__(self, n, chantype, ptime, dist, load, retry, backoff,
                 skew=SOURCE_NOSKEW, qmax=0, simtime=10000):
        WirelessNetwork.__init__(self, n, chantype, ptime, dist, load, retry, backoff,
                                 skew, qmax, simtime)
    def make_node(self, loc, retry):
        return TDMANode(loc, self, retry)

################################################################

if __name__ == '__main__':
    random.seed(6172538) # uncomment this line for repeatability
    ## Task 3.2 to Task 3.5
    ## TODO: modify the below parameters
    gui = True
    numnodes = 16
    simtime = 10000
    ptime = 1
    load = 100
    retry = False
    skew = False
    
    wnet = TDMAWirelessNetwork(numnodes, 'TDMA', ptime,
                               'exponential', load, retry, 'None',
                               skew, 0, simtime)
    if gui == True:
        sim = NetSim()
        sim.SetNetwork(wnet)
        sim.MainLoop()
    else:
        wnet.step(simtime)
        succ = []
        for node in wnet.nlist: succ.append(node.stats.success)
        for node in wnet.nlist:
            if node.stats.collisions > 0:
                print("ERROR! TDMA should not have collisions")
        ind = numpy.arange(len(wnet.nlist))
        width = 0.35
        p.bar(ind, succ, width, color = 'r')
        p.ylabel('Throughput')
        p.xlabel('Node #')
        p.show()
        time.sleep(5)
    os._exit(0)
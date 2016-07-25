#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

linkopts = ['core', 'aggr', 'edge', 'host']
linkval = [{'bw':10,'delay':'5ms'},{'bw':5, 'delay':'10ms'},{'bw':4, 'delay':'12ms'},{'bw':3, 'delay':'15ms'}]

def int2dpid( dpid ):
   try:
      dpid = hex( dpid )[ 2: ]
      dpid = '0' * ( 16 - len( dpid ) ) + dpid
      return dpid
   except IndexError:
      raise Exception( 'Unable to derive default datapath ID -Mayu - '
                       'please either specify a dpid or use a '
              'canonical switch name such as s23.' )


class DataCenter(Topo):       
   def create_tree(self):
      #Adding switches
      val = 0
      value = 0
      switch = []
      while val < self.maxlevel:
         while value < pow(self.fanout, val):
            switch.append(self.addSwitch('s' + str(val) + str(value)))
            value = value + 1
         value = 0
         val = val + 1
      print switch

      #Adding hosts
      host = []
      valH = 0
      while valH < pow(self.fanout, self.maxlevel):
         host.append(self.addHost('h' + str(valH)))
         valH = valH + 1
      print host
      
      #Adding link between host(s) n a switch
      if len(switch) == 1:
         valL = 0
         while valL < self.fanout:
            self.addLink(switch[0], host[valL])
            valL = valL + 1
      else:
         valS = 0
         valF = 0
         val = 0
         counter = 1 
         #Adding link between switches
         while val < len(switch)-1:
            while valF < self.fanout:
               val = valS + valF + counter 
               self.addLink(switch[valS], switch[val])
               valF = valF + 1
               print switch[valS]   
            valS = val - counter
            valF = 0
            counter = counter + 1
         print counter

         #Adding link between hosts n switches
         valHS = 0
         valFS = 0
         val = len(switch) - pow(self.fanout, self.maxlevel-1)
         loop = 0
         while valHS < len(host):
            while valFS < self.fanout:
                va = valHS + valFS
                self.addLink(switch[val + loop], host[va])
                valFS = valFS + 1
            valHS = valHS + self.fanout  
            valFS = 0
            loop = loop + 1
     
   def __init__(self, fanout, maxlevel, **opts):
      Topo.__init__(self, **opts)
      self.fanout = fanout
      self.maxlevel = maxlevel      
      core = self.addSwitch('core', dpid=int2dpid(1) )
      self.create_tree() 
          
topos = { 'dcgeneric': ( lambda:DataCenter(3, 3) )}


#class DataCenterPerf(Topo):  
  # def create_tree(self):
      # FILL CODE HERE
  #    print 'a'   
   # def __init__(self, fanout,maxlevel, **opts):
    #  Topo.__init__(self, **opts)

     # self.fanout = fanout 
      #self.maxlevel = maxlevel
      
      #core = self.addSwitch('core', dpid=int2dpid(1) )
      #self.create_tree() 

#topos = { 'dcperf': ( lambda:DataCenterPerf() )}



   

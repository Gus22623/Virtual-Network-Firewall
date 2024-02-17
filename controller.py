from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, IPAddr6, EthAddr

log = core.getLogger()

# allocate a routing table for hosts
IPS = {
  "h10" : ("10.0.1.10", '00:00:00:00:00:01'),
  "h20" : ("10.0.2.20", '00:00:00:00:00:02'),
  "h30" : ("10.0.3.30", '00:00:00:00:00:03'),
  "serv1" : ("10.0.4.10", '00:00:00:00:00:04'),
  "hnotrust" : ("172.16.10.100", '00:00:00:00:00:05'),
  
  # new hosts and switch mappings
  "h40": ("10.0.4.20", '00:00:00:00:00:06'),
  "h50": ("10.0.5.30", '00:00:00:00:00:07'),
}

class Controller (object):
  """
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    print (connection.dpid)
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)
    #use the dpid to figure out what switch is being created
    if (connection.dpid == 1):
      self.s1_setup()
    elif (connection.dpid == 2):
      self.s2_setup()
    elif (connection.dpid == 3):
      self.s3_setup()
    elif (connection.dpid == 4):
      self.s4_setup()
    elif (connection.dpid == 5):
      self.s5_setup()
    elif (connection.dpid == 21):
      self.cores21_setup()
    elif (connection.dpid == 31):
      self.dcs31_setup()
    else:
      print ("UNKNOWN SWITCH")
      exit(1)

  def s1_setup(self):
    #put switch 1 rules here
    msg = of.ofp_flow_mod()
    msg.priority = 10
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(msg)


  def s2_setup(self):
    #put switch 2 rules here
    msg = of.ofp_flow_mod()
    msg.priority = 10
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(msg)
    

  def s3_setup(self):
    #put switch 3 rules here
    msg = of.ofp_flow_mod()
    msg.priority = 10
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(msg)
  
  def s4_setup(self):
    #put switch 4 rules here
    msg = of.ofp_flow_mod()
    msg.priority = 10
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(msg)
  
  def s5_setup(self):
    #put switch 5 rules here
    msg = of.ofp_flow_mod()
    msg.priority = 10
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(msg)


  def cores21_setup(self):
    #put core switch rules here
    
    # Drop ICMP packets that are trying to go to hosts
    hnottrust_ICMP = of.ofp_flow_mod()
    hnottrust_ICMP.priority = 80 # Set the rule priority
    hnottrust_ICMP.match.dl_type = 0x0800 # IPv4
    hnottrust_ICMP.match.nw_proto = 1 # ICMP
    hnottrust_ICMP.match.nw_src = IPAddr("172.16.10.100") #Assign source address from hnotrust1 to drop ICMP
    hnottrust_ICMP.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER)) # Sends automatically to _handle_PacketIn
    self.connection.send(hnottrust_ICMP)
    
    # Drop any IP packets going to serv1
    hnottrust_IP = of.ofp_flow_mod()
    hnottrust_IP.priority = 70 # Set the rule priority
    hnottrust_IP.match.dl_type = 0x0800 # IPv4
    hnottrust_IP.match.nw_src = IPAddr("172.16.10.100") # Drop any IP packets from hnotrust1
    hnottrust_IP.match.nw_dst = IPAddr("10.0.4.10") #destination address to serv1 here
    hnottrust_IP.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER)) # Sends automatically to _handle_PacketIn
    self.connection.send(hnottrust_IP)
    
    #-----------------UDP Protocol-----------------
    
    
    # Drop all UDP packets within the network
    all_UDP = of.ofp_flow_mod()
    all_UDP.priority = 80
    all_UDP.match.dl_type = 0x0800  # IPv4
    all_UDP.match.nw_proto = 17  # UDP
    all_UDP.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
    self.connection.send(all_UDP)
    
    #-----------------------------------------------
    # List of IPs with corresponding port number
    ip = {'10.0.1.10':1, '10.0.2.20':2, '10.0.3.30':3, '10.0.4.10':4, '172.16.10.100':5}
    
    #traverse the IPs and assign destination to i and port to j
    for i,j in ip.items():
    	msg = of.ofp_flow_mod()
    	msg.priority = 30 # Set the rule priority
    	msg.match.dl_type = 0x0800 # IPv4
    	msg.match.nw_proto = 10 # ICMP
    	msg.match.nw_dst = i
    	msg.actions.append(of.ofp_action_output(port =j))
    	self.connection.send(msg)
    
    msg_i = of.ofp_flow_mod()
    msg_i.priority = 10
    msg_i.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(msg_i)


  def dcs31_setup(self):
    #put datacenter switch rules here
    msg = of.ofp_flow_mod()
    msg.priority = 10
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    self.connection.send(msg)

  #handle individual ARP packets
  #causes the switch to output packet_in on out_port
  def resend_packet(self, packet_in, out_port):
    msg = of.ofp_packet_out()
    msg.data = packet_in
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)
    self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Packets not handled by the router rules will be
    forwarded to this method to be handled by the controller
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    print ("Unhandled packet from " + str(self.connection.dpid) + ":" + packet.dump())

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Controller(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
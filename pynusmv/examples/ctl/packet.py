from pynusmv.model import *
import ipaddress

class Packet(Module):
  
     srcip = Var(Range(int(ipaddress.ip_address('0.0.0.0')),
                 int(ipaddres.ip_address('255.255.255.255'))))

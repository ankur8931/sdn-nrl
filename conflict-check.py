import requests
import json
import subprocess
from ipaddress import ip_network, ip_address

# Check layer2 overlap
def isL2subsetr2r1(l2s1, l2d1, l2s2, l2d2):
    if ((l2s1 == "" and l2s2 !="") or (l2d1 == "" and l2d2 != "")):
       return True
    return False

def isL2subsetr1r2(l2s1, l2d1, l2s2, l2d2):
    if ((l2s2 == "" and l2s1 !="") or (l2d2 == "" and l2d1 != "")):
       return True
    return False

def isL2equalsr1r2(l2s1, l2d1, l2s2, l2d2):
    if ((l2s1 == l2s2) and (l2d1 == l2d2)):         
       return True
    return False

# Check layer3 overlap
def isL3subsetr2r1(l3s1, l3d1, l3s2, l3d2):
    l3s1 = ip_network(l3s1)
    l3d1 = ip_network(l3d1)
    if (l3s2 in l3s1 and l3d2 in l3d1):
       return True
    return False

def isL3subsetr1r2(l3s1, l3d1, l3s2, l3d2):
    l3s2 = ip_network(l3s2)
    l3d2 = ip_network(l3d2)
    if (l3s1 in l3s2 and l3d1 in l3d2):
       return True
    return False
  
# Check layer4 overlap
def isL4subsetr2r1(l4s1, l4d1, l4s2, l4d2):
    if ((l4s2 == "" and l4s1 !="") or (l4d2 == "" and l4d1 != "")):
       return True
    return False

def isL4subsetr1r2(l4s1, l4d1, l4s2, l4d2):
    if ((l4s2 == "" and l4s1 !="") or (l4d2 == "" and l4d1 != "")):
       return True
    return False

def isL4equalsr1r2(l4s1, l4d1, l4s2, l4d2):
    if ((l4s1 == l4s2) and (l4d1 == l4d2)):         
       return True
    return False

# Check action matching

## Function for conflict checking
def conflict_detection(flows):

    for f_1 in flows:
        for f_2 in f_1:
    #total overlap/ partial overlap, same action, different action
            if f_1 !=f_2:

               #Extract action field for both rules
               a_1 = f_1['action']
               a_2 = f_2['action']
             

               # Extract rule1, rule2 layer2 fields
               f_1l2src = ''
               f_1l2dst = ''
               f_2l2src = ''
               f_2l2dst = ''
                 
               if 'ETH_SRC' in f_1.keys():
                   f_1l2src = f_1['ETH_SRC']
               if 'ETH_DST' in f_1.keys():
                   f_1l2dst = f_1['ETH_DST']
               if 'ETH_SRC' in f_2.keys():
                   f_2l2src = f_2['ETH_SRC']
               if 'ETH_DST' in f_2.keys():
                   f_2l2dst = f_2['ETH_DST']
                                    

               # Extract rule1, rule2 layer3 fields
                              
               f_1l3src = ''
               f_1l3dst = ''
               f_2l3src = ''
               f_2l3dst = ''

               if 'IPV4_SRC' in f_1.keys():
                   f_1l3src = f_1['IPV4_SRC']
               if 'IPV4_DST' in f_1.keys():
                   f_1l3dst = f_1['IPV4_DST']
               if 'IPV4_SRC' in f_2.keys():
                   f_2l3src = f_2['IPV4_SRC']
               if 'IPV4_DST' in f_2.keys():
                   f_2l3dst = f_2['IPV4_DST']

               # Extract rule1. rule2 layer4 fields
               
               f_1l4src = ''
               f_1l4dst = ''
               f_2l4src = ''
               f_2l4dst = ''

                
               if 'TCP_SRC' in f_1.keys():
                   f_1l4src = f_1['TCP_SRC']
               if 'TCP_DST' in f_1.keys():
                   f_1l4dst = f_1['TCP_DST']
               if 'TCP_SRC' in f_2.keys():
                   f_2l4src = f_2['TCP_SRC']
               if 'TCP_DST' in f_2.keys():
                   f_2l4dst = f_2['TCP_DST']

               # Check for inheritance conflict
               if ((isL2subsetr2r1(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst) or
                   isL2equalsr1r2(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst))
                   and (isL3subsetr2r1(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst) or
                   isL3equalsr1r2(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst))
                   and (isL4subsetr2r1(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst) or
                   isL4equalsr1r2(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst))):
                    
                     print("Inheritance: R2 is subset of R1")
                                     
               elif ((isL2subsetr1r2(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst) or
                   isL2equalsr1r2(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst))
                   and (isL3subsetr1r2(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst) or
                   isL3equalsr1r2(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst))
                   and (isL4subsetr1r2(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst) or
                   isL4equalsr1r2(f_1l2src, f_1l2dst, f_2l2src, f_2l2dst))):
                     
                     print("Inheritance: R2 is subset of R1")

                                 

flow1 = "http://192.168.3.30:8181/onos/v1/flows/"
r = requests.get(flow1, auth=('onos','rocks'))
flows = list()
print(r.status_code, r.reason)
print(r.text)
for flow in json.loads(r.text)['flows']:
    match = dict()
    if flow['selector']['criteria'][0]['type'] == 'IN_PORT':
       print("======Match======")
       if len(flow['selector']['criteria'])==1:
          print(flow['selector']['criteria'][0]['port'])
       else:
          field_len = len(flow['selector']['criteria'])
          for i in range(0,field_len):
              field_type = flow['selector']['criteria'][i]['type']
              if field_type == 'IN_PORT':
                 match[field_type] = flow['selector']['criteria'][i]['port']
              elif field_type == 'ETH_SRC' or field_type=='ETH_DST':
                 match[field_type] = flow['selector']['criteria'][i]['mac']
              elif field_type == 'IPV4_SRC' or field_type=='IPV4_DST':
                 match[field_type] = flow['selector']['criteria'][i]['ip']
              elif field_type == 'IP_PROTO':
                 match[field_type] = flow['selector']['criteria'][i]['protocol']
              elif field_type == 'TCP_SRC' or field_type =='TCP_DST':
                 match[field_type] = flow['selector']['criteria'][i]['tcpPort']
              elif field_type == 'UDP_SRC' or field_type =='UDP_DST':
                 match[field_type] = flow['selector']['criteria'][i]['udpPort']
          
       match['action'] = flow['treatment']['instructions'] 
    flows.append(match)
print(flows)              

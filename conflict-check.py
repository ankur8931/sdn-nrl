import requests
import json
import subprocess

'''cmd = 'ovs-ofctl dump-flows s1'
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
flows, err = p.communicate()
flows = flows.splitlines()

for flow in flows:
    if 'cookie' in flow:
       fields = flow.split(',')
       print(fields)

'''
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
                 
               
          
          #print(flow['selector']['criteria'][0]['port'])
          #print(flow['selector']['criteria'][1]['type'])
          #print(flow['selector']['criteria'][1]['mac'])
        
       print("======Action=====")
       print(flow['treatment']['instructions'])
       print('\n')
#print (r.text)
    flows.append(match)
print(flows)              

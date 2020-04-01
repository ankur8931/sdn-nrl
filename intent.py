import requests
import json

#Content type must be included in the header
header = {"content-type": "application/json"}

#url = "http://192.168.3.30:8181/onos/v1/flows/of:0000000000000001"
url = "http://192.168.3.30:8181/onos/v1/intents/"
#headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
'''
intent1 = {
  "id": "0x10",
  "type": "PointToPointIntent",
  "appId": "org.onosproject.cli",
  "selector": {
    "criteria": [
      {
        "type": "ETH_DST",
        "mac": "E2:99:5C:18:07:5B"
      }
    ]
  },
  "treatment": {
    "instructions": [
      {
        "type": "L2MODIFICATION",
        "subtype": "ETH_SRC",
        "mac": "A2:5D:5E:1C:A8:D9"
      }
    ]    
  },
  "priority": 55,
  "constraints": [
    {
      "inclusive": 'false',
      "types": ["OPTICAL"],
      "type": "LinkTypeConstraint"
    }
  ],
  "ingressPoint": {
    "port": "3",
    "device": "of:0000000000000001"
  },
  "egressPoint": {
    "port": "1",
    "device": "of:0000000000000001"
  }
}
'''
ingress = 'of:0000000000000001'
ingressPort = '3'
egress = 'of:0000000000000001'
egressPort = '1'
 
intentJsonTemplate = \
    '{{' + \
        '"type": "PointToPointIntent",' + \
        '"appId": "org.onosproject.cli",' + \
        '"ingressPoint": {{' + \
        '    "device": "{}",' + \
        '    "port": "{}"' + \
        '}},' + \
        '"egressPoint": {{' + \
        '    "device": "{}",' + \
        '    "port": "{}"' + \
        '}}' + \
    '}}'

intent1 = intentJsonTemplate.format(ingress, ingressPort, egress, egressPort)
#Switch ID needed for single flow
flow1 = {
  "priority": 5000,
  "isPermanent": 'true',
  "treatment": {
    "instructions": [
      {
        "type": "OUTPUT",
        "port": 2
      }
    ]
  },
  "selector": {
    "criteria": [
      {
        "type": "ETH_TYPE",
        "ethType": "0x84406"
      }
    ]
  }
}

r = requests.post(url, data=intent1, headers=header, auth=('onos', 'rocks'))
#r = requests.get(url, auth=('onos', 'rocks'))
print(r.status_code, r.reason)
print (r.text)

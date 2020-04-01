import requests
import json

#Content type must be included in the header
header = {"content-type": "application/json"}

#url = "http://192.168.3.30:8181/onos/v1/flows/of:0000000000000001"
url = "http://192.168.3.30:8181/onos/v1/intents/"
#headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
intent1 = {
  "type": "PointToPointIntent",
  "appId": "org.onosproject.core",
  "selector": {
    "criteria": [
      {
        "type": "ETH_DST",
        "mac": "86:2D:E8:3A:B5:02"
      }
    ]
  },
  "treatment": {
    "instructions": [
      {
        "type": "L2MODIFICATION",
        "subtype": "ETH_SRC",
        "mac": "DA:F3:9B:C5:30:DE"
      }
    ],
    "deferred": []
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
    "port": "1",
    "device": "of:0000000000000001"
  },
  "egressPoint": {
    "port": "2",
    "device": "of:0000000000000001"
  }
}

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

#r = requests.post(url, data=json.dumps(intent1), headers=header, auth=('onos', 'rocks'))
r = requests.get(url, auth=('onos', 'rocks'))
print(r.status_code, r.reason)
print (r.text)

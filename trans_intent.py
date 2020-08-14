import json
f= open('data.json','r')
data = json.load(f)
f.close()
f2= open('mission.json','r')
miss = json.load(f2)
f2.close()
intent = open('intent.txt','w')
intent2 = open('intent2.txt','w')
all_hosts = []
hosts_dic={}
for i in range(len(data['hosts'])):
    temp_id = data['hosts'][i]['id']
    all_hosts.append(temp_id)
    hosts_dic[temp_id] = {'id':data['hosts'][i]['data']['locations'][0]['elementId'],
                          'ip': data['hosts'][i]['data']['ipAddresses'][0]}


for x in range(len(miss['missionRequirements'])):
    src = miss['missionRequirements'][x]['src']
    dst = miss['missionRequirements'][x]['dst']
    port = miss['missionRequirements'][x]['port']
    src = src.split('.')[2]
    dst = dst.split('.')[2]
    port = port.split(':')[1]
    srcIP = hosts_dic[src]['ip']
    dstIP = hosts_dic[dst]['ip']
    intent_set = {'intent'+str(x+1): {'type': 'HostToHost', 'ipSrc': srcIP, 'ipDst': dstIP,
                                    'tcpDst':port}}
    intent2.writelines("add-host-intent --ipSrc  "+srcIP+ " --ipDSt  "+dstIP+" --tcpDst "+
                       port +'\n')
    intent.writelines(json.dumps(intent_set))
intent.close()
intent2.close()


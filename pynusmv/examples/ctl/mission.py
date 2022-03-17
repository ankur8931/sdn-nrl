import json
f = open('network.json','r')
data = json.load(f)
switches = []
switches_dic ={}
all_hosts = []
hosts_dic ={}
links = []
#### Getting switches info ####
for i in range(len(data['switches'])):
    temp_id = data['switches'][i]['id']
    switches.append(temp_id)
    switches_dic[temp_id] = { 'id':data['switches'][i]['data']['id']}
#### Getting hosts info ####
for i in range(len(data['hosts'])):
    temp_id = data['hosts'][i]['id']
    all_hosts.append(temp_id)
    hosts_dic[temp_id] = data['hosts'][i]['data']['locations'][0]['elementId']
    print(i)

f2= open('mission.json','r')
miss = json.load(f2)
req = []

for x in range(len(miss['missionRequirements'])):
    src = miss['missionRequirements'][x]['src']
    dst = miss['missionRequirements'][x]['dst']
    src = src.split('.')[2]
    dst = dst.split('.')[2]
    for s in switches_dic:
	txt=[]
        if src in switches_dic[s]['hosts']:
            txt.append('        switch = ' +str(s)+ ' & src = ' + src +' & dst = ' + dst +';')
            


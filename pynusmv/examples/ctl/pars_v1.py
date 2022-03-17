import json
import networkx as nx
f= open('data.json','r')
data = json.load(f)
switches = []
switches_dic ={}
all_hosts = []
hosts_dic ={}
links = []
G = nx.Graph()
#### Getting switches info ####
for i in range(len(data['switches'])):
    temp_id = data['switches'][i]['id']#it holds the switch name. e.g. s1, s2,etc
    switches.append(temp_id)
    #getting the switch OF id
    switches_dic[temp_id] = { 'id':data['switches'][i]['data']['id']}
#### Getting hosts info ####
for i in range(len(data['hosts'])):
    temp_id = data['hosts'][i]['id'] #it holds the host name. e.g. h1, h2,etc
    all_hosts.append(temp_id)
    # adding the OF id and the host IP address
    hosts_dic[temp_id] = {'id':data['hosts'][i]['data']['locations'][0]['elementId'],
                          'ip': data['hosts'][i]['data']['ipAddresses'][0]}

#### Getting links info ####
for l in range(len(data['links'])):
    temp_links =() # to hold the extracted link and then examine it if its a duplicate or not
    # add nodes to graph
    G.add_edge(data['links'][l]['src']['device'], data['links'][l]['dst']['device'])
    temp_links = (data['links'][l]['src']['device'], data['links'][l]['dst']['device'])
#### because there are duplicate links (s1,s2) and (s2,s1) we need to add only 1 link ####
    if temp_links in links or temp_links[::-1] in links:
        continue
    links.append(temp_links)

f.close()
####checking which hosts are connected to which switch ####
for s in switches:
    temp_hosts = ()
    for h in all_hosts:
        if hosts_dic[h]['id'] == switches_dic[s]['id']: #checking the OF ID for the switch and the host
            G.add_edge(h,s)
            temp_hosts += (h,)
            hosts_dic[h]['switch'] = s
    switches_dic[s]['hosts'] = temp_hosts
print("The system has the following nodes:")
print(G.nodes)
print("The system has the following edges:")
print(G.edges)
print("Path that violates the mission requirments are as follows:")
for path in nx.all_simple_paths(G, source='h2', target='h4'):
    print(path)



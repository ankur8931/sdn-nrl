import json

f= open('data-nrl.json','r')
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

#### Getting links info ####
for l in range(len(data['links'])):
    temp_links =()
    temp_links = (data['links'][l]['src']['device'], data['links'][l]['dst']['device'])
#### because there are duplicate links (s1,s2) and (s2,s1) we need to add only 1 link ####
    if temp_links in links or temp_links[::-1] in links:
        print('found duplicate link')
        continue
    links.append(temp_links)

f.close()
####checking which hosts are connected to which switch ####
for s in switches:
    temp_hosts = ()
    for h in all_hosts:
        if hosts_dic[h] == switches_dic[s]['id']: #checking the OF id
            temp_hosts += (h,)
    switches_dic[s]['hosts'] = temp_hosts

f = open ("output.smv",'w')
# f.writelines("%s\n" % place for place in text)
f.writelines('MODULE main \n' \
#### defining the switch variable ####
        '   VAR switch: {')
for s in switches:
    if s!= switches[len(switches)-1]:
        f.writelines(s + ',')
f.writelines(switches[len(switches)-1] + "};\n")

#### defining the src hosts variable ####
f.writelines("       src: {")
for h in all_hosts:
    if h!= all_hosts[len(all_hosts)-1]:
        f.writelines(h + ',')
f.writelines(all_hosts[len(all_hosts)-1] + "};\n")

#### defining the dst hosts  variable ####
f.writelines("       dst: {")
for h in all_hosts:
    if h!= all_hosts[len(all_hosts)-1]:
        f.writelines(h + ',')
f.writelines(all_hosts[len(all_hosts)-1] + "};\n")

### building the switch state trnasition ###
f.writelines("ASSIGN\n   next(switch):= case\n")
for s in switches_dic:
    txt =[] #temporary variable to hold the writing.
    txt.append('        switch = ' +str(s)+ ' &(')
    for h in range(len(switches_dic[s]['hosts'])-1):
        th =switches_dic[s]['hosts'][h]
        txt.append( "dst !="+str(th) +' |')
    txt.append(" dst !=" +str(switches_dic[s]['hosts'][len(switches_dic[s]['hosts']) -1]) +"):")
    f.writelines(txt)
    txt = [] # reset the varialbe so we can use it to check for mulit switch connection
    for l in range(len(links)):
        if s in links[l]:
            if links[l].index(s) ==0:
                txt.append(links[l][1])
            else:
                txt.append(links[l][0])
#### we check if a switch is connected to more than one switch, then we specify the next state as
#### either of the connected states ####
    if len(txt)==1:
        f.writelines(txt)
        f.writelines(';')
    else:
        f.writelines(' {')
        for t in range(len(txt)-1):
            f.writelines(txt[t])
            f.writelines(',')
        f.writelines(txt[len(txt)-1])
        f.writelines("};")
    f.writelines('\n')
f.writelines("        TRUE: "+str(switches[0]) + ";\n   esac;\n")
f.writelines("   next(src):= src;\n")
f.writelines("   next(dst):= dst;\n")
f.writelines("INIT switch = "+ str(switches[0]) +';')
f.close()

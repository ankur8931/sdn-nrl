import pynusmv, json
from pynusmv.mc import check_ctl_spec, explain, eval_ctl_spec
f2= open('mission.json','r')
miss = json.load(f2)
sec_req ={}
##########
# Fetching security rules from missiion.json
#########
for x in range(len(miss['securityRules'])):
    src = miss['securityRules'][x]['src']
    dst = miss['securityRules'][x]['dst']
    src = src.split('.')[2]
    dst = dst.split('.')[2]
    sec_req['req'+str(x)] = {'src':src, 'dst':dst}

########
# computing the SMV module
########
pynusmv.init.init_nusmv()
pynusmv.glob.load_from_file("output.smv")
pynusmv.glob.compute_model()
fsm = pynusmv.glob.prop_database().master.bddFsm

print("total number of states:  " + str(fsm.count_states(fsm.init)))
############
# checking the conflict based on the security requirments in the mission.json 
############
for state in fsm.pick_all_states(fsm.init):
    for key in sec_req:
        if (state.get_str_values()['src'] ==sec_req[key]['src']) & (state.get_str_values()['dst'] ==sec_req[key]['dst']) &(state.get_str_values()['switch']== 's2'):
           print("found conflict between h2 & h4")
           print(state.get_str_values())

pynusmv.init.deinit_nusmv()



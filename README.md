# Software-Defined Networking Research
Goal of this project is to check network policy issues in a Software-Defined Networking based multi-controller cloud network.

intent.py - Used for extraction of intent from SDN controller

dataExtract.py - extracts the network topology information from json files with intent definition,
                 and converts the extracted information into SMV format that can be used for model checking

trans_intent.py - translates administrator specified high-level policies into network intents

mission.json - specifies the mission requirements or admin policies at high-level

bgp_ls.json - BGP router sample policies

SMV_inter.py - translates the output of mission policies into SMV according to security requirements

conflict_check.py - security policy conflict checking code

bgp_topo.py - mininet BGP topology generation code


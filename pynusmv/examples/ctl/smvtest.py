import pynusmv
with pynusmv.init.init_nusmv():
 pynusmv.glob.load_from_file("packet.smv") 
 pynusmv.glob.compute_model()


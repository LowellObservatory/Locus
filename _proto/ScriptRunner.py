'''
Created on May 4, 2018

@author: dlytle
'''
from ArcCamLib.ArcDSPCommands import ARC_command_list

class ScriptRunner(object):
    '''
    Run scripts by name on the current device.
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        self.parent = parent
        
        
    def runScript(self, script_name):
        pass
        with open(script_name, "r") as scrpt:
            for line in scrpt:
                self.executeLine(line)
                
    def executeLine(self, line):
#         self.parent.utilities.writeToConsole(line.rstrip(), "normal")
        bits = line.split()
        if (bits[0] == '#'): return()
        info = ARC_command_list[bits[0]]
#         self.parent.utilities.writeToConsole(
#             "call prefix " + info["call_prefix"], "normal")
        if (info["call_prefix"] == "none"):
            commandToExecute = "self.parent.device." + bits[0]
        else:
            commandToExecute = ("self.parent.device." + info["call_prefix"] +
                                "." + bits[0])
            
        commandToExecute += "("
        for i in range(info["num_args"]):
            commandToExecute += bits[i+1]
            if i+1 < info["num_args"]:
                commandToExecute += ","
        
        commandToExecute += ")"
        self.parent.utilities.writeToConsole(commandToExecute, "normal")
        exec(commandToExecute)
        pass
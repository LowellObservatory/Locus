'''
Created on May 1, 2018

@author: dlytle
'''

import stomp
import json
import time
import os
import numpy as np
from ArcCamLib.ArcCam import ArcCam
from PyQt5.QtGui import QTextCursor, QFont, QColor

class BrokerTalk(object):
    '''
    Communications with ActiveMQ Broker.
    '''

    def __init__(self, parent):
        
        '''
        Set up Stomp connection to broker and start listening.
        '''
        self.parent = parent
        BrokerIP = '10.10.100.24'     # Jumar
        StompPort = 61613             # Jumar Broker Stomp Port
        self.conn = stomp.Connection([(BrokerIP, StompPort)])
        self.conn.set_listener('', self.MyListener(self))
        self.conn.start()
        self.conn.connect()
        
        # Initialize the ArcCam object here because all the code we need
        # has been initialized by the time we get here.
        device = "/dev/Arc64PCI0"
        config_file = "/home/dlytle/git/ArcCam/src/config/CCD57.xml"
        self.parent.device = ArcCam("CCD57", self.parent, device, config_file)
        #self.parent.device.system.camera_open()

        self.conn.subscribe(destination='/topic/ProtoLOCUS/commands',
                       id=1, ack='auto')
        
    class MyListener(stomp.ConnectionListener):
        def __init__(self, parent):
            self.parent = parent
            pass
        def on_error(self, headers, message):
            print('received an error "%s"' % message)
        def on_message(self, headers, message):
            self.parent.parent.utilities.writeToConsole(message, "normal")
            self.parent.ReactToMessage(message)
            
            
    def ReactToMessage(self, message):
        if ("initialize" in message):
            device = "/dev/Arc64PCI0"
            config_file = "/home/dlytle/git/ArcCam/src/config/CCD57.xml"
            self.parent.device = ArcCam("CCD57", self.parent, device, config_file)
            
        if ("camera_open" in message):
            if(self.parent.device):
                self.parent.device.system.camera_open()
            else:
                self.parent.utilities.writeToConsole(
                    "Device not initialized", "error")
            
        if ("camera_close" in message):
            self.parent.device.system.camera_close()
            
        if ("status" in message):
            if(self.parent.device):
                rsp = self.parent.device.status()
                self.parent.utilities.writeToConsole(
                    "sending response = " + str(rsp), "response")
                self.conn.send(body=str(rsp),
                           destination='/topic/ProtoLOCUS/responses')
            else:
                self.parent.utilities.writeToConsole(
                    "Device not initialized", "error")
            
        if ("LOCUS_Exit" in message):
            self.conn.disconnect()
            os._exit(0)
        
        if ("run_script" in message):
            json_data = json.loads(message)
            self.parent.utilities.writeToConsole("running script " +
                                                 json_data["script_name"],
                                                 "normal")
            self.parent.scriptrunner.runScript(json_data["script_name"])
            
        if ("read_memory" in message):
            #self.parent.utilities.writeToConsole("Reading Memory!")
            json_data = json.loads(message)
    
            rsp = self.parent.device.simple.read_memory(json_data["board"],
                                         json_data["memory_type"],
                                         int(json_data["memory_address"], 16))
            
            self.parent.utilities.writeToConsole(
                "sending response = " + str(rsp), "response")
            
            self.conn.send(body=str(rsp),
                           destination='/topic/ProtoLOCUS/responses')
            
        if ("arccam_script" in message):
            json_data = json.loads(message)
            
            rsp = self.parent.scriptrunner.run_script(json_data["script_name"])


    def Send(self, message):
        self.conn.send(body=message, destination='/topic/ProtoLOCUS/responses')
        
    def returnImage(self, data, x, y):
        self.parent.utilities.writeToConsole(
                    "sending image back as text", "response")
        
        textArray = data.tolist()
        jsondata = {}
        jsondata['command'] = 'image_return'
        jsondata['exp_time'] = self.parent.device.camera_exposure_time
        jsondata['x'] = x
        jsondata['y'] = y
        jsondata['data'] = textArray
        json_data = json.dumps(jsondata)
        self.Send(json_data)
    
        
    def ExitBroker(self):
        self.conn.disconnect()
        
        
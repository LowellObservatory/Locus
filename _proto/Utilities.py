'''
Created on May 1, 2018

@author: dlytle
'''

import datetime
from time import sleep
from PyQt5.QtGui import QColor
from PIL import Image
import numpy as np

class Utilities(object):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        self.parent = parent
        
    def writeToConsole(self, theString, messageType):
        
        # Write a line into the console window.
        # If this message is an error message increase font size and color red.
        if ("error" in messageType):
            self.parent.logOutput.setTextColor(QColor('Red'))
            self.parent.logOutput.setFontPointSize(14.0)
        # If this message is a response, color it blue.
        elif("response" in messageType):
            self.parent.logOutput.setTextColor(QColor('blue'))
        elif("arccam" in messageType):
            self.parent.logOutput.setTextColor(QColor('green'))
            
        tstamp = datetime.datetime.now()
        self.parent.logOutput.insertPlainText(tstamp.strftime(
            "%Y-%m-%d %H:%M:%S") + ":  " + theString + "\n")
        sb = self.parent.logOutput.verticalScrollBar()
        sb.setValue(sb.maximum())
        sleep(0.01)
        self.parent.logOutput.setTextColor(QColor('Black'))
        self.parent.logOutput.setFontPointSize(10.0)
    
            
            
            
            
            
            
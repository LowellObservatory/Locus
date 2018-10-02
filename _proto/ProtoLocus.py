'''
Created on Apr 30, 2018

@author: dlytle
'''
from PyQt5.QtWidgets import (QWidget, QTextEdit, QApplication, QMessageBox,
                             QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QTextCursor, QFont, QColor
import sys
import stomp
from ArcCamLib.ArcCam import ArcCam
import time
import json
import os

from Locus.Utilities import Utilities
from Locus.BrokerTalk import BrokerTalk
from Locus.ScriptRunner import ScriptRunner

class ProtoLocus(QWidget):
    
    def __init__(self):
        
        super().__init__()
        
        self.device = None
        self.initUI()
        self.utilities = Utilities(self)
        self.brokertalk = BrokerTalk(self)
        self.scriptrunner = ScriptRunner(self)
        
        
        
    def initUI(self):
        # Logging window to log output.
        self.logOutput = QTextEdit(self)
        self.logOutput.setReadOnly(True)
        self.logOutput.setLineWrapMode(QTextEdit.NoWrap)
 
        font = self.logOutput.font()
        font.setFamily("Courier")
        font.setPointSize(10)
         
        #self.logOutput.moveCursor(QTextCursor.End)
         
        # Set up the quit button to exit the program.
        qbtn = QPushButton('Quit', self)
        qbtn.setToolTip('This button quits ProtoLocus')
        qbtn.clicked.connect(QApplication.instance().quit)
         
        # Put the quit button in a horizontal layout so it is far right.
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(qbtn)
         
        # Put all these graphics together into the main window.
        vbox = QVBoxLayout()
        vbox.addWidget(self.logOutput)
        vbox.addLayout(hbox1)
         
        # Set up main window, size, title, and show it.
        self.setLayout(vbox)
        self.setGeometry(100, 100, 1000, 420)
        self.setWindowTitle('ProtoLocus Console')
        self.show()
        self.logOutput.setTextColor(QColor('Black'))
        self.logOutput.setFontPointSize(10.0)
        #self.utilities.writeToConsole("Locus Ready", "normal")
        
        
    def closeEvent(self, event):
         
        # If the user tries to close the program by clicking on the
        # window close button at the top of the window, check to see
        # if they really want to close and close if so.  The preferred
        # method of closing the main window is by using the "quit" button.
        reply = QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
 
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
            
if __name__ == '__main__':
    
    # Run the program.
    app = QApplication(sys.argv)
    ex = ProtoLocus()
    sys.exit(app.exec_())
        
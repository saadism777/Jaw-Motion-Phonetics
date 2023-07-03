import os
import signal
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication,QLabel,QDesktopWidget,QHBoxLayout, QCheckBox, QVBoxLayout, QFileDialog
import socket
import time
import sys
from subprocess import Popen
from PyQt5.QtCore import QTimer, Qt

#Initializign variables
front_proc = None
front_face_width = None
front_path = None
def start_or_stop_processes(start):
    global front_proc
    if start:
        # Start the two subprocesses and return the objects
        if front_face_width is not None:
            front_proc = Popen(['python', 'app.py', str(front_face_width), str(front_path)])
        
    else:
        print("Missing values")

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 300)
        self.center()
        self.setWindowTitle("Jaw  Motion Phonetics")
        self.label = QtWidgets.QLabel("Enter the front face width value:")
        self.entry = QtWidgets.QLineEdit()
        
        self.labelB = QLabel("Select Input File: ")
        self.buttonB = QtWidgets.QPushButton('Browse File')
        self.buttonB.clicked.connect(self.showFileDialog)


        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFont(font)
        self.button = QtWidgets.QPushButton("OK", clicked=self.get_entry_value)
        self.button2 = QtWidgets.QPushButton("Exit", clicked=self.close_app)
     

        layout = QVBoxLayout(self)
        
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.labelB)
        layout.addWidget(self.buttonB)
       
        layout.addWidget(self.button)
        layout.addWidget(self.button2)

    def showFileDialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.fileSelected.connect(self.fileSelectedAction)
        file_dialog.exec_()
    
    def fileSelectedAction(self, filepath):
        # Do something with the filepath
        global front_path
        front_path=filepath
        self.labelB.setText(f"Selected file: {front_path}")

 
    def center(self):
        # Get the geometry of the screen
        screen = QDesktopWidget().screenGeometry()

        # Calculate the center position of the screen
        center_x = screen.width() // 2
        center_y = screen.height() // 2

        # Move the window to the center of the screen
        self.move(center_x - self.width() // 2, center_y - self.height() // 2)
    def get_entry_value(self):
        global front_face_width, side_face_width
        front_face_width = float(self.entry.text())
        # Use the face_width value in your application
        print("The front face width is:", front_face_width)
       
        # Launch both apps
        # Example usage:
        start_or_stop_processes(True)
        #self.start_subprocess()
    
    def close_app(self):
        # Stop the two subprocesses
        #if front_proc and side_proc is not None:
        #    start_or_stop_processes(False)
        timer = QTimer(self)
        timer.timeout.connect(QApplication.quit)
        timer.start(500)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
